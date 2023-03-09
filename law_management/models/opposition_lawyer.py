# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class OppositionLawyer(models.Model):
    _name = 'opposition.lawyer'
    _rec_name = 'opposition_lawyer_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    # _inherits = {
    #     'res.users': 'user_id',
    # }

    # user_id = fields.Many2one(
    # 'res.users', string='Related User', required=True,
    # ondelete='cascade', help='User-related data of the Claimant/Plaintiff Lawyer',store=True)
    opposition_id = fields.Char(string='Opposition ID',readonly=True , copy=False)
    opposition_lawyer_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=True)
    image = fields.Binary(string='Image', attachment=True)
    opposition_lawyer_type = fields.Selection([('organisation', 'Organisation'), ('individual', 'Individual')], default='organisation' , string='Type', track_visibility='onchange')
    ol_or_company_reg_id = fields.Char(string='Company Regis. ID')
    ol_or_country_reg_id = fields.Many2one(
        'res.country', string='Country of Registration', ondelete='restrict', track_visibility='onchange')
    opposition_lawyer_nationality = fields.Many2one('nationality.master',string='Nationality')
    opposition_lawyer_nationality_code = fields.Char(related='opposition_lawyer_nationality.nationality_code',string='Nationality Code')
    opposition_phone = fields.Char(string='Phone', track_visibility='onchange')
    opposition_mobileP = fields.Char(
        string='Mobile', track_visibility='onchange')
    opposition_mobileW = fields.Char(
        string='Mobile', track_visibility='onchange')
    opposition_emailP = fields.Char(
        string='Email', track_visibility='onchange')
    opposition_emailW = fields.Char(
        string='Email', track_visibility='onchange')
    opposition_website = fields.Char(
        string='Website', track_visibility='onchange')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one(
        'res.country.state', string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(string='zip',
                      track_visibility='onchange')
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict', track_visibility='onchange')
    village = fields.Char(string='Village', track_visibility='onchange')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')
    district_id = fields.Char(string='District', track_visibility='onchange')
    account_details_ids = fields.One2many(
        'account.master', 'opp_lawyer_account', string='Account')
    opp_lawyer_doc_ids = fields.One2many(
        'opp.lawyer.document', 'opp_lawyer_document_id', string='Documents')
    postal_street = fields.Char(string='Postal Street')
    postal_street2 = fields.Char(string='Postal Street2..')
    postal_city_id = fields.Char(string='Postal City')
    postal_village = fields.Char(string='Village')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict')
    postal_zip = fields.Char(string='Postal zip')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    postal_district_id = fields.Char(string='District', track_visibility='onchange')
    ol_doc_count = fields.Integer(
        compute="_compute_ldoc_count", string='Document')
    opp_lawyer_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    copy_address = fields.Boolean(string='Copy Physical Address', default=False, track_visibility='onchange')

    @api.model
    def create(self, values):
        if values.get('opposition_lawyer_name', ''):
            values['opposition_id'] = self.env['ir.sequence'].next_by_code('opposition.lawyer')
            name = values.get('opposition_lawyer_name', '')
            values['name'] = name
            login = values.get('opposition_emailW', '')
            if login:
                values['login'] = login
            if not login:
                values['login'] = values['opposition_id']
            values['user_type'] = 'claimant_plaintiff_lawyer'
            values['groups_id'] = []
        res = super(OppositionLawyer, self).create(values)
        if res.opposition_mobileP:
            mobile1 = res.opposition_mobileP
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if res.opposition_mobileW:
            mobile2 = res.opposition_mobileW
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_user_claimant_plaintiff_lawyer')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res


    @api.multi
    def write(self, values):
        if values.get('opposition_mobileP', ''):
            mobile1 = values.get('opposition_mobileP', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if values.get('opposition_mobileW', ''):
            mobile2 = values.get('opposition_mobileW', '')
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(OppositionLawyer, self).write(values)

    @api.onchange('copy_address')
    def onchange_copy_address(self):
        if self.copy_address == True:
            self.postal_street = self.street or ''
            self.postal_street2 = self.street2 or ''
            self.postal_city_id = self.city_id or ''
            self.postal_village = self.village or ''
            self.postal_district_id = self.district_id or ''
            self.postal_state_id  = self.state_id.id or ''
            self.postal_zip  = self.zip or ''
            self.postal_country_id = self.country_id.id or ''
        if self.copy_address == False:
            self.postal_street = ''
            self.postal_street2 = ''
            self.postal_city_id = ''
            self.postal_village = ''
            self.postal_district_id = ''
            self.postal_state_id  = ''
            self.postal_zip  = ''
            self.postal_country_id = ''



    @api.onchange('opposition_emailP', 'opposition_emailW')
    def validate_mail(self):
        if self.opposition_emailP:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.opposition_emailP)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')
        if self.opposition_emailW:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.opposition_emailW)
            if match == None:
                raise ValidationError('Work E-mail ID is Not Valid!!!')

    # Button
    @api.multi
    def action_opposition_lawyer_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('opp_lawyer_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'opp_lawyer',
                                  'default_opp_lawyer_account': self.id or False})
            return action

    @api.multi
    def action_opp_lawyer_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.opp_lawyer_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('opp_lawyer_document_id', 'in', [self.id])]
            action['context'] = ({'default_opp_lawyer_document_id': self.id})
            return action

    # Count
    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('opp_lawyer_account', '=', partner.id)])

    @api.multi
    def _compute_ldoc_count(self):
        DocLine = self.env['opp.lawyer.document']
        for doc in self:
            doc.ol_doc_count = DocLine.search_count(
                [('opp_lawyer_document_id', '=', doc.id)])


class OppLawyerDocument(models.Model):
    _name = 'opp.lawyer.document'
    _order = 'create_date desc'
    _rec_name = 'opp_lawyer_document_id'
    _inherit = ['mail.thread']

    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment', string='Attachments')
    comment = fields.Text(string='Description')
    date = fields.Date(string='Date')
    ol_d_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    opp_lawyer_document_id = fields.Many2one(
        'opposition.lawyer', string='Claimant/Plaintiff Lawyer')