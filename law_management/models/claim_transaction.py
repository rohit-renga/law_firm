# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class ClaimDistributeTransaction(models.Model):
    _name = "claim.distribution.transaction"
    _order = 'create_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name" , readonly=True , copy=False)
    claim_distribution_id = fields.Many2one("claim.distribution", string="Claim Distribution ID")
    transaction_date = fields.Date(string="Date")
    transaction_amount = fields.Float(string="Amount")
    paid_to_whom = fields.Selection([
                            ('client', 'Client'),
                            ('court', 'Court')], string="Paid to whom")
    paid_by = fields.Selection([
                            ('accuse', 'Claimant / Plaintiff'),
                            ('court', 'Court')], string="Paid By")
    client_id = fields.Many2one("client.client", related='claim_distribution_id.client_id', string="Client")    
    accuse_id = fields.Many2one("accuse.details", related='claim_distribution_id.accuse_id', string="Claimant / Plaintiff")
    attachments = fields.Binary(string="Attachment")
    debit_account_id = fields.Many2one("account.master", string="Account Debited")
    credit_account_id = fields.Many2one("account.master", string="Account Credited")
    payment_mode = fields.Selection([
                            ('cash', 'Cash'),
                            ('bank', 'Bank'),
                            ('cheque', 'Cheque')], string="Mode of payment")
    cheque_no = fields.Char(string="Cheque Number")
    bank_transaction_no = fields.Char(string="Bank Transfer Transaction Number")
    case_id = fields.Many2one("matter.matter", related='claim_distribution_id.case_id', string="Case ID")
    receipt_no = fields.Char(string="Receipt Number")
    transaction_ref = fields.Char(string="Transaction Reference")
    t_court_id = fields.Many2one('court.court', related='claim_distribution_id.court_id', string="Court")
    payment_schedule_id = fields.Many2one("payment.schedule", string="Payment schedule", domain="[('claim_distribution_id', '=', claim_distribution_id)]")       

    @api.model
    def create(self, values):
        if values.get('claim_distribution_id', ''):
            values['name'] = self.env['ir.sequence'].next_by_code('claim.distribution.transaction') or ''
        res = super(ClaimDistributeTransaction, self).create(values)
        return res

    @api.onchange('client_id')
    def _onchange_client_id(self):
        domain = {}
        items_list = []
        for item in self.claim_distribution_id.client_id:
            items_list.append(item.id)
        domain = { 'client_id': [ ('id', 'in', items_list) ] } 
        return { 'domain': domain }

    @api.onchange('t_court_id','paid_to_whom','paid_by','accuse_id')
    def _onchange_debit_id(self):
        items_list = []
        if(self.t_court_id and self.paid_to_whom == 'client' and not self.accuse_id):
            return {'domain': {'debit_account_id':[('id', 'in', [account.id for account in self.env['account.master'].search([]) if account.account_holder == 'court'  and account.court_id.id ==self.t_court_id.id and self.paid_to_whom == 'client'])]}}
        elif( self.accuse_id and self.paid_to_whom == 'court'):
            return {'domain': {'debit_account_id':[('id', 'in', [account.id for account in self.env['account.master'].search([]) if account.account_holder == 'accuse'  and self.paid_to_whom == 'court' and account.accuse_account.id ==self.accuse_id.id])]}}
    
    @api.onchange('t_court_id','paid_to_whom','paid_by','client_id')
    def _onchange_credit_id(self):
        items_list = []
        if(self.t_court_id and self.paid_by == 'accuse' and not self.client_id):
            return {'domain': {'credit_account_id':[('id', 'in', [account.id for account in self.env['account.master'].search([]) if account.account_holder == 'court'  and account.court_id.id ==self.t_court_id.id and self.paid_by == 'accuse'])]}}
        elif( self.client_id and self.paid_by == 'court'):
            return {'domain': {'credit_account_id':[('id', 'in', [account.id for account in self.env['account.master'].search([]) if account.account_holder == 'client'  and self.paid_by == 'court' and account.client_account.id ==self.client_id.id])]}}
    
    @api.onchange('accuse_id')
    def _onchange_accuse_id(self):
        domain = {}
        items_list = []
        for item in self.claim_distribution_id.accuse_id:
            items_list.append(item.id)
        domain = { 'accuse_id': [ ('id', 'in', items_list) ] } 
        return { 'domain': domain }