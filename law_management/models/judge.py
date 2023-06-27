# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import re

class JudgeDetail(models.Model):
    _name = 'judge.details'
    _rec_name = 'judge_name'
    _order = 'create_date desc'
    _description = 'Judge'
    _inherit = ['mail.thread']
    _inherits = {
        'res.users': 'user_id',
    }

    user_id = fields.Many2one(
    'res.users', string='Related User', required=False,
    ondelete='cascade', help='User-related data of the patient',store=True)
    judge_id = fields.Char(string='Judge ID' , readonly=True , copy=False)
    image = fields.Binary(string='Image', attachment=True)
    judge_name = fields.Char(string='Name',track_visibility='onchange')
    practice_id = fields.Char(string='Practice ID')
    judge_mobileP = fields.Char(string='Mobile', track_visibility='onchange')
    judge_mobileW = fields.Char(string='Mobile', track_visibility='onchange')
    judge_emailP = fields.Char(string='Email', track_visibility='onchange')
    judge_emailW = fields.Char(string='Email', track_visibility='onchange')
    judge_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    judge_experience = fields.Char(
        string='Experience', track_visibility='onchange')
    start_date = fields.Date(string='To Date' ,default=fields.Date.today())
    end_date = fields.Date(string='From Date')
    previous_court = fields.Char(string='Previous Court')
    judge_details_id = fields.Many2one('court.court', string='Court')
    judge_createed_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    case_detail_ids = fields.One2many('matter.matter', 'judge_id', string='Case Details')
    judge_registrar_id = fields.Many2one('registrar.details',string='Registrar')
    judge_secretary_id = fields.Many2one('secretary.details',string='Court Reporter')
    judge_registrar_phone = fields.Char(related='judge_registrar_id.registrar_phone', string='Phone')
    judge_registrar_mobile = fields.Char(related='judge_registrar_id.registrar_mobile', string='Mobile')
    judge_registrar_email = fields.Char(related='judge_registrar_id.registrar_email', string='Email')
    judge_secretary_phone = fields.Char(related='judge_secretary_id.secretary_phone',string='Phone')
    judge_secretary_mobile = fields.Char(related='judge_secretary_id.secretary_mobile',string='Mobile')
    judge_secretary_email = fields.Char(related='judge_secretary_id.secretary_email',string='Email')

    _sql_constraints = [('name_uniq', 'UNIQUE(practice_id)', 'Practice ID Must Be Unique!!!')]

    
    @api.model
    def create(self, values):
        if values.get('judge_name', ''):
            values['judge_id'] = self.env['ir.sequence'].next_by_code('judge.details')
            name = values.get('judge_name', '')
            values['name'] = name
            login = values.get('judge_emailW', '')
            if login:
                values['login'] = login
            values['user_type'] = 'judge'
            values['groups_id'] = []
        res = super(JudgeDetail, self).create(values)
        if res.judge_mobileP:
            mobile1 = res.judge_mobileP
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if res.judge_mobileW:
            mobile2 = res.judge_mobileW
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        group_user = self.env.ref('law_management.group_law_firm_user_judge')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res


    @api.multi
    def write(self, values):
        if values.get('judge_mobileP', ''):
            mobile1 = values.get('judge_mobileP', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        if values.get('judge_mobileW', ''):
            mobile2 = values.get('judge_mobileW', '')
            if mobile2.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(JudgeDetail, self).write(values)


    @api.onchange('judge_emailP','judge_emailW')
    def validate_mail(self):
        if self.judge_emailP:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.judge_emailP)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')
        if self.judge_emailW:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.judge_emailW)
            if match == None:
                raise ValidationError('Work E-mail ID is Not Valid!!!')