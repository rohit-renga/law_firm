# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class ClientClient(models.Model):
    _name = 'client.client'
    _order = 'create_date desc'
    _rec_name = 'client_name'
    _inherit = ['mail.thread']
    _description = 'Client'
    # _inherits = {
    #     'res.users': 'user_id',
    # }

    # user_id = fields.Many2one(
    # 'res.users', string='Related User', required=False,
    # ondelete='cascade', help='User-related data of the Client',store=True)
    client_id = fields.Char(string='client ID' , readonly=True , copy=False)
    client_name = fields.Char(string='Name', track_visibility='onchange')
    client_type = fields.Selection([('organisation', 'Organisation'), ('individual', 'Individual')], default='organisation' , string='Type', track_visibility='onchange')
    image = fields.Binary(string='Image', attachment=True)
    client_phone = fields.Char(string='Phone' , track_visibility='onchange')
    client_mobileP = fields.Char(
        string='Mobile', track_visibility='onchange')
    client_mobileW = fields.Char(
        string='Mobile(Work)', track_visibility='onchange')
    client_emailP = fields.Char(
        string='Email ID', track_visibility='onchange' )
    client_emailW = fields.Char(
        string='Email ID(Work)', track_visibility='onchange')
    client_website = fields.Char(string='Website', track_visibility='onchange')
    client_nationality = fields.Many2one('nationality.master',string='Nationality')
    client_nationality_code = fields.Char(related='client_nationality.nationality_code',string='Nationality Code')
    traditional_authority = fields.Char(string="Traditional Authority")
    client_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    client_dob = fields.Date(
        string='Birthdate', track_visibility='onchange')
    client_age = fields.Char(
        string='Age', track_visibility='onchange')
    client_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')

    # case_ids = fields.One2many('matter.matter','client_name', string="case")
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(
        string='Street2..', track_visibility='onchange')
    city_id = fields.Char(
        string='City', track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')

    village = fields.Char(string='Village', track_visibility='onchange')
    state_id = fields.Many2one('res.country.state',
                               string='State', track_visibility='onchange')
    zip = fields.Char(string='zip',
                      track_visibility='onchange')
    country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')
    account = fields.Integer(
        string='Account', compute='_compute_account_count')
    account_details_ids = fields.One2many(
        'account.master', 'client_account', string='Account')
    client_doc_ids = fields.One2many(
        'client.document', 'client_document_id', string='Documents')
    relative_info = fields.Char(string="Relative Info")
    relative_name = fields.Char(string="Relative Name")
    active = fields.Boolean(string="Active", default=True)
    case = fields.Integer(compute="_compute_matter_count", string='Case')
    postal_street = fields.Char(string='Postal Street')
    postal_street2 = fields.Char(string='Postal Street2..')
    postal_city_id = fields.Char(string='Postal City')
    postal_village = fields.Char(string='Village')
    postal_district_id = fields.Char(string='District', track_visibility='onchange')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict')
    postal_zip = fields.Char(string='Postal zip')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    c_doc_count = fields.Integer(
        compute="_compute_cdoc_count", string='Document')
    client_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    # client_name_many = fields.Many2many('client.client', "matter_client_rel", "matter_id", "client_id", string='Client')
    case_ids=fields.Many2many('matter.matter', "matter_client_rel", "client_id", "matter_id", string="case")
    copy_address = fields.Boolean(string='Copy Physical Address', default=False, track_visibility='onchange')


    @api.one
    def _compute_cases(self):
        import pdb; pdb.set_trace()
        related_recordset = self.env["matter.matter"].search([("id", "in",case_ids.client_name_many)])
        self.client_cases_ids = related_recordset


    @api.model
    def create(self, values):
        if values.get('client_name', ''):
            values['client_id'] = self.env['ir.sequence'].next_by_code('client.client')
            name = values.get('client_name', '')
            values['name'] = name
            login = values.get('client_emailP', '')
            if login:
                values['login'] = login
        user_type = values.get('client_type', '')
        if user_type == 'client':
            values['user_type'] = 'client'
        if user_type == 'organisation':
            values['user_type'] = 'organisation'
        values['groups_id'] = []
        res = super(ClientClient, self).create(values)
        if res.client_mobileP:
            mobile1 = res.client_mobileP
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if res.client_mobileW:
            mobile2 = res.client_mobileW
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_user_client')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res


    @api.multi
    def write(self, values):
        if values.get('client_mobileP', ''):
            mobile1 = values.get('client_mobileP', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if values.get('client_mobileW', ''):
            mobile2 = values.get('client_mobileW', '')
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(ClientClient, self).write(values)

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

    @api.onchange('client_dob')
    def onchange_client_dob(self):
        if self.client_dob:
            b_date = datetime.strptime(self.client_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.client_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    
    @api.onchange('client_emailP','client_emailW')
    def validate_mail(self):
        if self.client_emailP:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.client_emailP)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')
        if self.client_emailW:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.client_emailW)
            if match == None:
                raise ValidationError('Work E-mail ID is Not Valid!!!')

    #Button
    @api.multi
    def client_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('client_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'client',
                                  'default_client_account': self.id or False,})
            return action


    @api.multi
    def action_case_matter_form_view(self):
        return {
            'name': _('Case'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'matter.matter',
            'type': 'ir.actions.act_window',
            'domain': [('client_name_many', 'in', self.id)],
            'context': {'default_client_name': self.id,
                        'tree_view_ref': self.env.ref('law_management.view_matter_matter_tree'),
                        'form_view_ref': self.env.ref('law_management.view_matter_matter_form')},
        }

    @api.multi
    def action_client_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.client_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('client_document_id', 'in', [self.id])]
            action['context'] = ({'default_client_document_id': self.id})
            return action

    #Count
    @api.multi
    def _compute_matter_count(self):
        matter = self.env['matter.matter']
        for case in self:
            case.case = matter.search_count([('client_name_many', 'in', case.id)])

    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('client_account', '=', partner.id)])

    @api.multi
    def _compute_cdoc_count(self):
        DocLine = self.env['client.document']
        for doc in self:
            doc.c_doc_count = DocLine.search_count(
                [('client_document_id', '=', doc.id)])


class accountLines(models.Model):
    _name = 'account.lines'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _rec_name = 'account_num'

    account_name_line = fields.Char(string="Account name")
    account_num = fields.Char(string="Account Number")
    bank_of_account_line = fields.Char(string="Bank")
    account_line_id = fields.Many2one('client.client')


class ClientDocumentsType(models.Model):
    _name = 'client.document.type'

    name = fields.Char()



class ClientDocuments(models.Model):
    _name = 'client.document'
    _order = 'create_date desc'
    _rec_name = 'client_document_id'
    _inherit = ['mail.thread']
    
    doc_name = fields.Many2one('client.document.type', 'Document Type')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description')
    date = fields.Date(string='Date')
    cd_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    client_document_id = fields.Many2one('client.client', string='Client Name')
    category_id = fields.Many2one('document.category')