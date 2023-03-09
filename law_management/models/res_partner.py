# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import math


class ClientResPartner(models.Model):
    _inherit = 'res.partner'

    mobileW = fields.Char(string='Mobile(Work)')
    emailW = fields.Char(string='Email(Work)')
    type = fields.Selection(
        [('client', 'Client'), ('lawyer', 'Lawyer'), 
        ('judge', 'Judge'), ('witness', 'Witness'), 
        ('accuse', 'Claimant / Plaintiff'), 
        ('plaintiff', 'Plaintiff'),
        ('opposition','Opposition')], default="client", string='Customer')
    dob = fields.Date(string='Birthdate', track_visibility='onchange')
    age = fields.Char(string='Age', track_visibility='onchange')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    
    marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
    passportno = fields.Char(
        string='Passport No.', track_visibility='onchange')
    govidtype = fields.Many2one('government.proof.type',string='ID Proof Type')
    govidno = fields.Char(
        string='ID Proof No.', track_visibility='onchange')
    case_matter_count = fields.Integer(
        "Case", compute='_compute_case_matter_count')
    identity_document_ids = fields.One2many(
        'identity.documents', 'customer_indentity_document', string='Identity Documents')

    @api.onchange('dob')
    def onchange_dob(self):
        if self.dob:
            b_date = datetime.strptime(self.dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.multi
    def action_case_matter_form_view(self):
        return {
            'name': _('Case / Matter'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'matter.matter',
            'type': 'ir.actions.act_window',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id,
                        'tree_view_ref': self.env.ref('law_management.view_matter_matter_tree'),
                        'form_view_ref': self.env.ref('law_management.view_matter_matter_form')},
        }

    @api.multi
    def _compute_case_matter_count(self):
        CaseMatterLine = self.env['matter.matter']
        for partner in self:
            partner.case_matter_count = CaseMatterLine.search_count(
                [('partner_id', '=', partner.id)])

class IndentiryDocument(models.Model):
    _name = 'identity.documents'

    id_type = fields.Selection([('national_id', 'National ID'), ('passport', 'Passport'), (
        'driving_license', 'Driving License'), ('other', 'Other')], default='driving_license',string='ID Type')
    other_id = fields.Char(string='Other ID')
    id_proof_no = fields.Char(string='ID Proof No.')
    attach_id = fields.Binary(string='Attachments')
    customer_indentity_document = fields.Many2one('res.partner',string='Identity Document')

# class CustomerForm(models.Model):
#     _inherit = 'res.partner'

#     customer_name = fields.Char("Name", required=True)