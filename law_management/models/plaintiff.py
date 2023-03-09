# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

import re

class PlaintiffDetails(models.Model):
    _name = 'plaintiff.details'
    _order = 'create_date desc'
    _rec_name = 'plaintiff_name'
    _inherit = ['mail.thread']

    plaintiff_id = fields.Char(string='Plaintiff ID')
    image = fields.Binary(string='Image', attachment=True)
    plaintiff_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=True)
    plaintiff_mobile = fields.Char(
        string='Mobile', track_visibility='onchange', required=True)
    plaintiff_email = fields.Char(
        string='Email ID', track_visibility='onchange')
    plaintiff_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    plaintiff_website = fields.Char(
        string='Website', track_visibility='onchange')

    plaintiff_dob = fields.Date(
        string='Birthdate', track_visibility='onchange')
    plaintiff_age = fields.Char(string='Age', track_visibility='onchange')
    plaintiff_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
    plaintiff_note = fields.Text(
        string='Notes...', track_visibility='onchange')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one(
        'res.country.state', string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(string='zip',
                      track_visibility='onchange')
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict', track_visibility='onchange')
    plaintiff_doc_ids = fields.One2many(
        'plaintiff.document', 'plaintiff_document_id', string='Documents')
    p_doc_count = fields.Integer(
        compute="_compute_pdoc_count", string='Document')
    plaintiff_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    _sql_constraints = [('name_uniq', 'UNIQUE(plaintiff_mobile,plaintiff_email)', 'Mobile No. & Email-ID Must Be Unique!')]

    @api.model
    def create(self, values):
        if values.get('plaintiff_mobile', ''):
            mobile = values.get('plaintiff_mobile', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(PlaintiffDetails, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('plaintiff_mobile', ''):
            mobile = values.get('plaintiff_mobile', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(PlaintiffDetails, self).write(values)

    @api.onchange('plaintiff_dob')
    def onchange_plaintiff_dob(self):
        if self.plaintiff_dob:
            b_date = datetime.strptime(self.plaintiff_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.plaintiff_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.onchange('plaintiff_email')
    def validate_mail(self):
       if self.plaintiff_email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.plaintiff_email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

    # Button
    @api.multi
    def action_plaintiff_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.plaintiff_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('plaintiff_document_id', 'in', [self.id])]
            action['context'] = ({'default_plaintiff_document_id': self.id})
            return action

    # Count
    @api.multi
    def _compute_pdoc_count(self):
        DocLine = self.env['plaintiff.document']
        for doc in self:
            doc.p_doc_count = DocLine.search_count(
                [('plaintiff_document_id', '=', doc.id)])

class PlaintiffDocument(models.Model):
    _name = 'plaintiff.document'
    _rec_name = 'doc_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_id = fields.Many2many('ir.attachment', string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    pd_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    plaintiff_document_id = fields.Many2one(
        'plaintiff.details', string='Lawyer Document')
