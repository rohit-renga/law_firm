# coding: utf-8

from odoo import models, fields, api, _


class Department(models.Model):
    _name = 'department.department'

    name = fields.Char('Department')


class Clinet(models.Model):
    _inherit = 'client.client'

    department_id = fields.Many2one('department.department', 'Ministry/Department')
    contact_person = fields.Char('Contact Person')
    contact_phone = fields.Char('Phone number')

class Claimant(models.Model):
    _inherit = 'accuse.details'

    name_claimant_firm = fields.Char('Name of claimant/ Firm')
    nationality = fields.Many2one('res.country','Nationality')
    national_id = fields.Char('National ID')
    contact_details = fields.Text('Contact Details')