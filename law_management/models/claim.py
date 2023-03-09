# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError, Warning

class MatterClaim(models.Model):
    _name = "matter.claim"
    _rec_name = 'name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Claim'


    # claim_seq = fields.Char(
    #     size=256, string='Claim Seq', readonly=True, default='New Matter', copy=False)
    name = fields.Char(size=256, string='Claim ID', readonly=True, default='New Claim', copy=False)
    case_id = fields.Many2one("matter.matter", string="Case Number")
    claim_case_name = fields.Char(related='case_id.case_name', string="Case Name")
    description = fields.Text(string="Description")
    client_name = fields.Many2many('client.client', related='case_id.client_name_many', string='Client')
    accuse_name = fields.Many2many('accuse.details', related='case_id.accuse_ids', string="Claimant / Plaintiff")
    claim_amount = fields.Float(string="Amount Claimed by Plaintiff")
    paid_amount = fields.Float(string="Amount decided by the Judge against the above Claimed")
    claim_count = fields.Float(string="Claim Distribution", compute="_compute_claim_count")
    court_id = fields.Many2one('court.court',related='case_id.court_id',string="Court")
    claim_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    remainig_claim_amount_count = fields.Float(string="Savings Amount", compute="count_remainig_amount", readonly=True)
    claim_categories = fields.Selection(
        [('interest', 'Interest'), ('legal_collection_fee', 'Legal Collection Cost/Fee'), ('party_cost', 'Party and Party Cost')], default="interest", string='Categories', track_visibility='onchange')


    @api.one
    @api.depends('claim_amount','paid_amount')
    def count_remainig_amount(self):
        self.remainig_claim_amount_count = self.claim_amount-self.paid_amount


    @api.model
    def create(self,vals):
        res = super(MatterClaim,self).create(vals)
        if not vals['claim_amount'] > 0.0:
            raise Warning(_('The "Total Claim Amount" value must be strictly positive.'))
        if not vals['paid_amount'] > 0.0:
            raise Warning(_('The "Amount to be Paid as Per Judgement" value must be strictly positive.'))
        sequence_code = self.env['ir.sequence'].next_by_code('matter.claim')
        res.update({'name':sequence_code})
        return res
    
    @api.multi
    def write(self, vals):
        res = super(MatterClaim, self).write(vals)
        if (self.paid_amount and self.claim_amount) <= 0.00:
            raise ValidationError(_('Amount must be strictly positive.'))
        else:
            return res

    @api.multi
    def action_view_claim_distribution(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.claim_distribution_action')
        if action_rec:
            remain_amount = (self.claim_amount - self.paid_amount) if self.claim_amount and self.paid_amount else 0.0
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('claim_id','in', [self.id])]
            action['context'] = ({'default_claim_id':self.id,})
            return action

    @api.multi
    def _compute_claim_count(self):
        claim_data = self.env['claim.distribution'].search([('claim_id', '=', self.id)])
        if claim_data:
            self.claim_count = len(claim_data)