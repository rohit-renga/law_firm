# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class CaseClerk(models.Model):
    _name = 'case.clerk'
    _rec_name = 'case_clerk_name'
    # _order = 'create_date desc'
    _inherit = ['mail.thread']
    _inherits = {
        'res.users': 'user_id',
    }

    user_id = fields.Many2one(
    'res.users', string='Related User', required=True,
    ondelete='cascade', help='User-related data of the Case Clerk',store=True)
    image = fields.Binary(string='Image', attachment=True)
    case_clerk_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=True)
    case_clerk_id = fields.Char(string='ID' , readonly=True , copy=False)
    clerk_mobile = fields.Char(
        string='Mobile', track_visibility='onchange')
    clerk_email = fields.Char(
        string='Email', track_visibility='onchange')
    clerk_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    clerk_dob = fields.Date(string='Birthdate', track_visibility='onchange')
    clerk_age = fields.Char(string='Age', track_visibility='onchange')
    clerk_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
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
    district_id = fields.Char(string='District', track_visibility='onchange')
    active = fields.Boolean(
        default=True, help="The active field allows you to hide the category without removing it.")
    postal_street = fields.Char(string='Postal Street')
    postal_street2 = fields.Char(string='Postal Street2..')
    postal_city_id = fields.Char(string='Postal City')
    postal_village = fields.Char(string='Village')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict')
    postal_zip = fields.Char(string='Postal zip')
    postal_district_id = fields.Char(string='District', track_visibility='onchange')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    copy_address = fields.Boolean(string='Copy Physical Address', default=False, track_visibility='onchange')
         
    @api.model
    def create(self, values):
        if values.get('case_clerk_name', ''):
            values['case_clerk_id'] = self.env['ir.sequence'].next_by_code('case.clerk')
            name = values.get('case_clerk_name', '')
            values['name'] = name
            login = values.get('clerk_email', '')
            if login:
                values['login'] = login
            values['user_type'] = 'case_clerk'
            values['groups_id'] = []
        res = super(CaseClerk, self).create(values)
        if res.clerk_mobile:
            mobile1 = res.clerk_mobile
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_case_clerk')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res


    @api.multi
    def write(self, values):
        if values.get('clerk_mobile', ''):
            mobile1 = values.get('clerk_mobile', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(CaseClerk, self).write(values)


    @api.onchange('clerk_dob')
    def onchange_clerk_dob(self):
        if self.clerk_dob:
            b_date = datetime.strptime(self.clerk_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.clerk_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.onchange('clerk_email')
    def validate_mail(self):
        if self.clerk_email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.clerk_email)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')


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
        