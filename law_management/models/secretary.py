# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import re



class SecretaryrDetails(models.Model):
    _name = 'secretary.details'
    _order = 'create_date desc'
    _description = 'Court Reporter'
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Name')
    secretary_id = fields.Char(string='ID' , readonly=True , copy=False)
    secretary_email  = fields.Char(string='Email')
    secretary_phone  = fields.Char(string='Phone')
    secretary_mobile = fields.Char(string='Mobile')

    
    @api.model
    def create(self, values):
        if values.get('name', ''):
            values['secretary_id'] = self.env['ir.sequence'].next_by_code('secretary.details') or ''
        res = super(SecretaryrDetails, self).create(values)
        if res.secretary_mobile:
            mobile1 = res.secretary_mobile
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return res


    @api.multi
    def write(self, values):
        if values.get('secretary_mobile', ''):
            mobile1 = values.get('secretary_mobile', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(SecretaryrDetails, self).write(values)
