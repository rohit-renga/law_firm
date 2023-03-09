# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class PaymentSchedule(models.Model):
    _name = "payment.schedule"
    _rec_name = 'name'
    _order = 'case_id asc'
    _inherit = ['mail.thread']

    name = fields.Char(string="Payment Milestone ID")
    schedule_date = fields.Date(string="Schedule Date of Payment")
    description = fields.Text(string="Description")
    paid_amount = fields.Float(string="Amount")
    paid_by = fields.Selection([
                            ('accused', 'Claimant / Plaintiff'),
                            ('court', 'Court')], string="Paid By")
    claim_distribution_id = fields.Many2one("claim.distribution", string="Claim Distribution ID")
    is_paid = fields.Boolean(string="Is Paid")
    case_id = fields.Many2one(related='claim_distribution_id.case_id', string="Case Number")
    court_id = fields.Many2one(related='claim_distribution_id.court_id', string="Court")
    payment_case_name = fields.Char(related='case_id.case_name', string='Case Name')
    state = fields.Selection([('draft', 'Draft'), ('judgement_completed', 'Judgement Completed'),('treasury', 'Treasury'),('payment_completed', 'Payment Completed')], default='draft', string='State',track_visibility='onchange')
    payment_category = fields.Selection([('principal_bebt', 'Principal Debt'), ('interest', 'Interest'),('legal_fee', 'Legal Collection Cost/Fee'),('party_cost','Party and Party Cost'),('part_payment','Part-payment')], default='principal_bebt', string='Category',track_visibility='onchange')


    @api.model
    def create(self,vals):
        res = super(PaymentSchedule,self).create(vals)
        sequence_code = self.env['ir.sequence'].next_by_code('payment.schedule')
        res.update({'name':sequence_code})
        return res


    @api.multi
    def action_button_judgement(self):
        if self.state == 'draft':
            self.state = 'judgement_completed'

    @api.multi
    def action_button_treasury(self):
        if self.state == 'judgement_completed':
            self.state = 'treasury'

    @api.multi
    def action_payment_completed(self):
        if self.state == 'treasury':
            self.state = 'payment_completed'

