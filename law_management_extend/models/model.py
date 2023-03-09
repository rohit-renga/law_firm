# coding: utf-8

from odoo import models, fields, api, _



class lawyer(models.Model):
    _inherit = 'lawyer.details'

    national_id = fields.Char('National ID')
    name_lawyer = fields.Char('Name')


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


class Defendant(models.Model):
    _inherit = 'accuse.details.defendant'

    name_claimant_firm = fields.Char('Name of claimant/ Firm')
    nationality = fields.Many2one('res.country','Nationality')
    national_id = fields.Char('National ID')
    contact_details = fields.Text('Contact Details')

class Opposition(models.Model):
    _inherit = 'opposition.lawyer'

    national_id = fields.Char('National ID')
    contact_details = fields.Text('Contact Details')

class Case(models.Model):
    _inherit = 'matter.matter'

    file_owner = fields.Selection([('lawyer', 'Lawyer'), ('opposition', 'Claimant/Plaintiff Lawyer'), ('client', 'Client'), ('accuse', 'Claimant / Plaintiff'), ('judge', 'Judge'), ('witness', 'Witness'),('registry','Registry')], string="Current File Owner",track_visibility='onchange')
    registry_options = fields.Selection([('archived','Archived'),
                                         ('attorney_general','Attorney General'),
                                         ('director','Director of Civil Litigation'),
                                         ('paid_files','Paid Files / Concluded Files'),
                                         ('registry_payment','Registry Payment Pending'),
                                         ])