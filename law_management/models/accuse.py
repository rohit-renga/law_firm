# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class AccuseDetails(models.Model):
    _name = 'accuse.details'
    _rec_name = 'accuse_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Plaintiff'

    accuse_id = fields.Char(string='Claimant / Plaintiff' , readonly=True , copy=False)
    image = fields.Binary(string='Image', attachment=True)
    accuse_name = fields.Char(string='Name',track_visibility='onchange', required=True)
    accuse_type = fields.Selection([('organisation', 'Organisation'), ('individual', 'Individual')], default='organisation' , string='Type', track_visibility='onchange')
    company_registration_no = fields.Char(string='Company Registration No.')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')

    account_details_ids = fields.One2many(
        'account.master', 'accuse_account', string='Account')
    accuse_document_ids = fields.One2many(
        'accuse.document', 'accuse_document_id',string='Documents')

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
        'matter.matter', 'accused', string='Cases')#, domain=lambda self: [('case_result','=','on_going')])
    # won_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases won', domain=lambda self: [('case_result','=','won')])
    # lost_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases lost', domain=lambda self: [('case_result','=','lost')])
    # settlement_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases settled', domain=lambda self: [('case_result','=','settlement')])
    

    @api.model
    def create(self, values):
        if values.get('accuse_name', ''):
            values['accuse_id'] = self.env['ir.sequence'].next_by_code('accuse.details') or ''
        res = super(AccuseDetails, self).create(values)
        return res


    #Button
    @api.multi
    def action_accuse_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'accuse',
                                  'default_accuse_account': self.id or False})
            return action

    @api.multi
    def action_accuse_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.accuse_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_document_id', 'in', [self.id])]
            action['context'] = ({'default_accuse_document_id': self.id})
            return action

    #Count
    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('accuse_account', '=', partner.id)])

    @api.multi
    def _compute_adoc_count(self):
        DocLine = self.env['accuse.document']
        for doc in self:
            doc.a_doc_count = DocLine.search_count(
                [('accuse_document_id', '=', doc.id)])

class AccuseName(models.Model):
    _name = 'accuse.name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',required=True,track_visibility='onchange')

class AccuseIDocument(models.Model):
    _name = 'accuse.document'
    _rec_name = 'accuse_document_id'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    
    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments',track_visibility='onchange')
    comment = fields.Text(string='Description',track_visibility='onchange')
    date = fields.Date(string='Date',default=fields.Date.today())
    ad_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    accuse_document_id = fields.Many2one('accuse.details',string='Claimant / Plaintiff Document')