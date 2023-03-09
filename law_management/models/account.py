# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class Account(models.Model):
    _name = 'account.master'
    _rec_name = 'account_number'
    _description = 'Account'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    account_seq_id = fields.Char(
        size=256, string='Account Seq', readonly=True, default='Account Seq', copy=False)
    account_number = fields.Char(string='Account Number',track_visibility='onchange')
    client_account = fields.Many2one('client.client',string='Payee(Client)',track_visibility='onchange')
    lawyer_account = fields.Many2one('lawyer.details',string='Payee(Lawyer)',track_visibility='onchange')
    opp_lawyer_account = fields.Many2one('opposition.lawyer',string='Claimant/Plaintiff Lawyer Payee',track_visibility='onchange')
    accuse_account = fields.Many2one('accuse.details',string='Payee(Claimant / Plaintiff)',track_visibility='onchange')
    court_account = fields.Many2one('court.court',string='Payee(Court)',track_visibility='onchange')
    account_type = fields.Many2one('account.type', string='Account Type',track_visibility='onchange')
    bank = fields.Many2one('res.bank', string='Bank',track_visibility='onchange')
    IFSC_code = fields.Char(string='IFSC code',track_visibility='onchange')
    SWIFT_code = fields.Char(string='SWIFT code',track_visibility='onchange')
    account_holder = fields.Selection([
        ('client', 'Client'),
        ('lawyer', 'Lawyer'),
        ('opp_lawyer', 'Claimant/Plaintiff Lawyer'),
        ('accuse', 'Claimant/Plaintiff'),
        ('court', 'Court')],string='Account Holder Type',track_visibility='onchange')
    person = fields.Char()
    account_master_id = fields.Many2one('client.client',track_visibility='onchange')
    court_id = fields.Many2one('court.court',track_visibility='onchange')
    date = fields.Date(string='Date',default=fields.Date.today(),readonly=True)
    account_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    account_holder_name = fields.Char(compute="_get_account_holder_name")

    _sql_constraints = [('name_uniq', 'UNIQUE(account_number)', 'Account No. Must Be Unique!')]

    
    @api.model
    def create(self, values):
        if values.get('account_number', ''):
            values['account_seq_id'] = self.env['ir.sequence'].next_by_code('account.master') or ''
        res = super(Account, self).create(values)
        return res


    @api.multi
    def _get_account_holder_name(self):
        for name in self:
            name.account_holder_name = name.client_account.client_name or \
            name.lawyer_account.lawyer_name or name.opp_lawyer_account.opposition_lawyer_name \
             or name.accuse_account.accuse_name or name.court_id.court_name

class AccountType(models.Model):
    _name = 'account.type'
    _rec_name = 'name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Account Type',required=True,track_visibility='onchange')
    date = fields.Date(string='Date',default=fields.Date.today(),readonly=True)
    account_type_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Account Type Must Be Unique!')]