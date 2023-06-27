# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class RegistrarDetails(models.Model):
    _name = 'registrar.details'
    _order = 'create_date desc'
    _description = 'Registrar'
    _inherit = ['mail.thread']
    # _inherits = {
    #     'res.users': 'user_id',
    # }

    # user_id = fields.Many2one(
    # 'res.users', string='Related User', required=False,
    # ondelete='cascade', help='User-related data of the Registrar',store=True)
    name = fields.Char()
    registrar_id = fields.Char(string='Registrar ID' , readonly=True , copy=False)
    registrar_name = fields.Char(string='Name',track_visibility='onchange')
    image = fields.Binary(string='Image', attachment=True)
    ph_street = fields.Char(string='Street', track_visibility='onchange')
    ph_street2 = fields.Char(
        string='Street2..', track_visibility='onchange')
    ph_city_id = fields.Char(
        string='City', track_visibility='onchange')
    ph_district_id = fields.Char(string='District', track_visibility='onchange')

    ph_village = fields.Char(string='Village', track_visibility='onchange')
    ph_state_id = fields.Many2one('res.country.state',
                               string='State', track_visibility='onchange')
    ph_zip = fields.Char(string='zip',
                      track_visibility='onchange')
    ph_country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')
    po_street = fields.Char(string='Street', track_visibility='onchange')
    po_street2 = fields.Char(
        string='Street2..', track_visibility='onchange')
    po_city_id = fields.Char(
        string='City', track_visibility='onchange')
    po_district_id = fields.Char(string='District', track_visibility='onchange')

    po_village = fields.Char(string='Village', track_visibility='onchange')
    po_state_id = fields.Many2one('res.country.state',
                               string='State', track_visibility='onchange')
    po_zip = fields.Char(string='zip',
                      track_visibility='onchange')
    po_country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')
    registrar_email  = fields.Char(string='Email' )
    registrar_phone  = fields.Char(string='Phone')
    registrar_mobile = fields.Char(string='Mobile')
    registrar_website = fields.Char(string='Website')
    copy_address = fields.Boolean(string='Copy Physical Address', default=False, track_visibility='onchange')
    category = fields.Selection([('Judge','Judge'),
                                 ('Registrar','Registrar'),
                                 ('Magistrate','Magistrate'),
                                 ('Chairperson','Chairperson'),
                                 ('Justice of Appeal','Justice of Appeal')],string="Category")
        
    
    @api.model
    def create(self, values):
        if values.get('registrar_name', ''):
            values['registrar_id'] = self.env['ir.sequence'].next_by_code('registrar.details')
            name = values.get('registrar_name', '')
            values['name'] = name
            login = values.get('registrar_email', '')
            if login:
                values['login'] = login
            values['user_type'] = 'registrar'
            values['groups_id'] = []
        res = super(RegistrarDetails, self).create(values)
        if res.registrar_mobile:
            mobile1 = res.registrar_mobile
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_user_registrar')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res
   
    @api.multi
    def write(self, values):
        if values.get('registrar_mobile', ''):
            mobile = values.get('registrar_mobile', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(RegistrarDetails, self).write(values)
        self.id.write({'name':self.name},{'registrar_email':self.registrar_email})

    @api.onchange('copy_address')
    def onchange_copy_address(self):
        if self.copy_address == True:
            self.po_street = self.ph_street or ''
            self.po_street2 = self.ph_street2 or ''
            self.po_city_id = self.ph_city_id or ''
            self.po_village = self.ph_village or ''
            self.po_district_id = self.ph_district_id or ''
            self.po_state_id  = self.ph_state_id.id or ''
            self.po_zip  = self.ph_zip or ''
            self.po_country_id = self.ph_country_id.id or ''
        if self.copy_address == False:
            self.po_street = ''
            self.po_street2 = ''
            self.po_city_id = ''
            self.po_village = ''
            self.po_district_id = ''
            self.po_state_id  = ''
            self.po_zip  = ''
            self.po_country_id = ''