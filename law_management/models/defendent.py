# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class AccuseDetailsDefendant(models.Model):
    _name = 'accuse.details.defendant'
    _rec_name = 'accuse_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Plaintiff'

    accuse_id = fields.Char(string='Claimant / Plaintiff' , readonly=True , copy=False)
    image = fields.Binary(string='Image', attachment=True)
    accuse_name = fields.Char(string='Name',track_visibility='onchange', required=False)
    accuse_type = fields.Selection([('organisation', 'Organisation'), ('individual', 'Individual')], default='organisation' , string='Type', track_visibility='onchange')
    company_registration_no = fields.Char(string='Company Registration No.')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')

    account_details_ids = fields.One2many(
        'account.master', 'accuse_account_defendant', string='Account')
    accuse_document_ids = fields.One2many(
        'accuse.document', 'accuse_document_defendant_id',string='Documents')

    a_doc_count = fields.Integer(
        compute="_compute_adoc_count", string='Document',track_visibility='onchange')
    accuse_nationality = fields.Many2one('nationality.master',string='Nationality')
    accuse_nationality_code = fields.Char(related='accuse_nationality.nationality_code',string='Nationality Code')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one('res.country.state',string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')
    country_id = fields.Many2one('res.country',string='Country', ondelete='restrict', track_visibility='onchange')
    village = fields.Char(string='Village', track_visibility='onchange')
    postal_street = fields.Char(string='Postal Street',track_visibility='onchange')
    postal_street2 = fields.Char(string='Postal Street2..',track_visibility='onchange')
    postal_city_id = fields.Char(string='Postal City',track_visibility='onchange')
    postal_village = fields.Char(string='Village',track_visibility='onchange')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict',track_visibility='onchange')
    postal_zip = fields.Char(string='Postal zip')
    district_id = fields.Char(string='District', track_visibility='onchange')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict',track_visibility='onchange')
    accuse_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    all_case_ids = fields.One2many(
        'matter.matter', 'accused_defendent', string='Cases')#, domain=lambda self: [('case_result','=','on_going')])
    # won_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases won', domain=lambda self: [('case_result','=','won')])
    # lost_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases lost', domain=lambda self: [('case_result','=','lost')])
    # settlement_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases settled', domain=lambda self: [('case_result','=','settlement')])
    

    @api.model
    def create(self, values):
        if values.get('accuse_name', ''):
            values['accuse_id'] = self.env['ir.sequence'].next_by_code('accuse.details.defendant') or ''
        res = super(AccuseDetailsDefendant, self).create(values)
        return res


    #Button
    @api.multi
    def action_accuse_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_account_defendant', '=', self.id)]
            action['context'] = ({'default_account_holder': 'accuse',
                                  'default_accuse_account_defendant': self.id or False})
            return action

    @api.multi
    def action_accuse_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.accuse_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_document_defendant_id', 'in', [self.id])]
            action['context'] = ({'default_accuse_document_defendant_id': self.id})
            return action

    #Count
    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('accuse_account_defendant', '=', partner.id)])

    @api.multi
    def _compute_adoc_count(self):
        DocLine = self.env['accuse.document']
        for doc in self:
            doc.a_doc_count = DocLine.search_count(
                [('accuse_document_defendant_id', '=', doc.id)])

class AccountMaster(models.Model):
    _inherit = 'account.master'

    accuse_account_defendant = fields.Many2one('accuse.details.defendant',string='Claimant / Plaintiff Document')


class AccuseDocument(models.Model):
    _inherit = 'accuse.document'

    accuse_document_defendant_id = fields.Many2one('accuse.details.defendant',string='Claimant / Plaintiff Document')

class Mater(models.Model):
    _inherit = 'matter.matter'

    accused_defendent = fields.Many2one('accuse.details.defendant',string='Defendant')
    