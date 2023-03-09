# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class ClaimDistribution(models.Model):
    _name = "claim.distribution"
    _order = 'create_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread']
    _description = 'Claim Distribute'

    name = fields.Char(string="Claim Distribute ID")
    claim_id = fields.Many2one("matter.claim", string="Claim ID")
    case_id = fields.Many2one("matter.matter", related='claim_id.case_id', string="Case Number")
    distribution_case_name = fields.Char(related='case_id.case_name', string='Case Name')
    paid_amount = fields.Float(string="Amount to be paid as per judgement", required=True)
    client_id = fields.Many2one("client.client", string="Client Name")
    accuse_id = fields.Many2one("accuse.details", string="Claimant / Plaintiff")
    validity_date_amount = fields.Float(string="Paid Amount to court till date", compute="_compute_remain_amount_court")
    remain_amount_court = fields.Float(string="Remaining Amount to Court(Loss/Saving)", compute="_compute_remain_amount_court")
    customer_amount = fields.Float(string="Paid Amount to Customer")
    remain_customer_amount = fields.Float(string="Remaining Amount for customer")
    transaction_line = fields.One2many("claim.distribution.transaction","claim_distribution_id", string="Claim Distribute Transaction")
    payment_schedule_line = fields.One2many("payment.schedule","claim_distribution_id", string="Payment Schedule")
    claim_trans_count = fields.Float(string="Claim Transaction", compute="_compute_claim_trans_count")
    payment_schedule_count = fields.Float(string="Payment Schedule", compute="_compute_payment_schedule_count")
    paid_amount_client = fields.Float(string="Paid Amount to Claimant / Plaintiff till date", compute="_compute_remain_amount_court")
    remain_amount_client = fields.Float(string="Remaining Amount to Claimant / Plaintiff", compute="_compute_remain_amount_court")
    court_id = fields.Many2one('court.court', related='claim_id.court_id', string="Court")

    @api.onchange('claim_id')
    def _onchange_accuse_id(self):
        domain = {}
        item_ids_list = []
        for item in self.claim_id.accuse_name:
            item_ids_list.append(item.id)
        domain = { 'accuse_id':[('id', 'in', item_ids_list)]}
        return {'domain': domain }

    @api.onchange('claim_id')
    def _onchange_client_id(self):
        domain = {}
        items_list = []
        for item in self.claim_id.client_name:
            items_list.append(item.id)
        domain = {'client_id': [('id', 'in', items_list)]} 
        return {'domain': domain}

    
    @api.model
    def create(self,vals):
        res = super(ClaimDistribution,self).create(vals)
        sequence_code = self.env['ir.sequence'].next_by_code('claim.distribution')
        res.update({'name':sequence_code})
        case_data = self.env['matter.claim'].search([('id', '=', res.claim_id.id)])
        claim_data = self.env['claim.distribution'].search([('claim_id', '=', res.claim_id.id)])
        total_paid_amount = sum([i.paid_amount for i in claim_data if i.paid_amount])
        if (total_paid_amount and case_data.paid_amount) and (case_data.paid_amount >= total_paid_amount):
            return res
        else:
            raise ValidationError(_('Paid amount more then claim paid amount.'))

    @api.multi
    def write(self, vals):
        res = super(ClaimDistribution, self).write(vals)
        case_data = self.env['matter.claim'].search([('id', '=', self.claim_id.id)])
        claim_data = self.env['claim.distribution'].search([('claim_id', '=', self.claim_id.id)])
        total_paid_amount = sum([i.paid_amount for i in claim_data if i.paid_amount])
        if (total_paid_amount and case_data.paid_amount) and (case_data.paid_amount >= total_paid_amount):
            return res
        else:
            raise ValidationError(_('Paid amount more then claim paid amount.'))

    @api.depends('transaction_line')
    def _compute_claim_trans_count(self):
        for rec in self:
            rec.claim_trans_count = len(rec.transaction_line)

    @api.depends('payment_schedule_line')
    def _compute_payment_schedule_count(self):
        for rec in self:
            rec.payment_schedule_count = len(rec.payment_schedule_line)


    @api.depends('paid_amount')
    def _compute_remain_amount_court(self):
        for rec in self:
            transaction_amount_court = sum([trans.transaction_amount for trans in rec.transaction_line if trans.transaction_amount and trans.paid_to_whom == 'court'])
            transaction_amount_customer = sum([trans.transaction_amount for trans in rec.transaction_line if trans.transaction_amount and trans.paid_to_whom == 'client'])
            if (rec.paid_amount and transaction_amount_court):
                if (rec.paid_amount >= transaction_amount_court):
                    rec.remain_amount_court = (rec.paid_amount - transaction_amount_court)
                    rec.validity_date_amount = transaction_amount_court
                else:
                    raise ValidationError(_('Transaction amount more then amount to be paid'))

            if (rec.paid_amount and transaction_amount_customer):
                if (rec.paid_amount >= transaction_amount_customer):
                    rec.remain_amount_client = (rec.paid_amount - transaction_amount_customer)
                    rec.paid_amount_client = transaction_amount_customer
                else:
                    raise ValidationError(_('Transaction amount more then amount to be paid'))

    @api.multi
    def action_claim_transaction(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.claim_distribution_transaction_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('claim_distribution_id','in', [self.id])]
            action['context'] = ({'default_claim_distribution_id': self.id or False,
                                 # 'default_client_id':self.client_id.id or False,
                                 # 'default_accuse_id':self.accuse_id.id or False,
                                 # 'default_court_id':self.court_id.id or False,
                                 })
            return action

    @api.multi
    def action_payment_schedule(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.payment_schedule_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('claim_distribution_id','in', [self.id])]
            action['context'] = ({'default_claim_distribution_id': self.id or False,
                                  # 'default_case_id':self.case_id.id,
                                  # 'default_court_id':self.court_id.id,
                                  })
            return action