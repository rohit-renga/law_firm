# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class CourtAdmin(models.Model):
    _name = 'court.admin'
    _rec_name = 'court_admin_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _inherits = {
        'res.users': 'user_id',
    }

    user_id = fields.Many2one(
    'res.users', string='Related User', required=False,
    ondelete='cascade', help='User-related data of the patient',store=True)
    court_ids = fields.Many2many('court.court',string='Court')
    image = fields.Binary(string='Image', attachment=True)
    court_admin_id = fields.Char(string='ID' , readonly=True , copy=False)
    court_admin_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=False)
    admin_mobile = fields.Char(
        string='Mobile', track_visibility='onchange')
    admin_email = fields.Char(
        string='Email', track_visibility='onchange')
    admin_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    admin_dob = fields.Date(string='Birthdate', track_visibility='onchange')
    admin_age = fields.Char(string='Age', track_visibility='onchange')
    admin_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
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
    district_id = fields.Char(string='District', track_visibility='onchange')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    admin_court_ids = fields.Many2many('court.court',compute="print_court_ids", string="court Ids", store=True)


    @api.model
    def create(self, values):
        if values.get('court_admin_name', ''):
            values['court_admin_id'] = self.env['ir.sequence'].next_by_code('court.admin')
            name = values.get('court_admin_name', '')
            values['name'] = name
            login = values.get('admin_email', '')
            if login:
                values['login'] = login
            values['user_type'] = 'court_admin'
            values['groups_id'] = []
        res = super(CourtAdmin, self).create(values)
        if res.admin_mobile:
            mobile1 = res.admin_mobile
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_user_admin')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res


    @api.multi
    def write(self, values):
        if values.get('admin_mobile', ''):
            mobile1 = values.get('admin_mobile', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(CourtAdmin, self).write(values)
   

    @api.depends('court_ids','admin_court_ids')
    @api.multi
    def print_court_ids(self):
        self.admin_court_ids = [(6, 0, self.court_ids.ids)] 


    @api.onchange('admin_dob')
    def onchange_admin_dob(self):
        if self.admin_dob:
            b_date = datetime.strptime(self.admin_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.admin_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))


    @api.onchange('admin_email')
    def validate_mail(self):
        if self.admin_email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.admin_email)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')
        