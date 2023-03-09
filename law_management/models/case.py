# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class CaseStages(models.Model):
    _name = 'case.stages'
    _rec_name = 'case_stages'
    _order = 'case_sequence'
    _inherit = ['mail.thread']
    _description = 'Case Stage'

    case_stages = fields.Char(string='Stage Name',track_visibility='onchange')
    case_defalut_stage = fields.Boolean(string='Default Stage',track_visibility='onchange')
    case_sequence = fields.Integer(string='Case Sequence', default=1,track_visibility='onchange')
    date = fields.Date(string='Date',readonly=True , default=fields.Date.today())
    case_stages_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    # _sql_constraints = [('name_uniq', 'UNIQUE(account_number)', 'Account No. Must Be Unique!')]

class CasePriority(models.Model):
    _name = 'case.priority'
    _rec_name = 'case_priority'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    case_priority = fields.Char(string='Case Priority',track_visibility='onchange')
    case_description = fields.Text(string='Description',track_visibility='onchange')


class CaseCategory(models.Model):
    _name = 'case.category'
    _rec_name = 'name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Many2one('case.sub.categories',string='Child Category',track_visibility='onchange')
    code = fields.Char(string='Code',track_visibility='onchange')
    type = fields.Selection(
        [('civil', 'Civil')], string='Parent Category', defaault='civil')
    description = fields.Text(string='Description',track_visibility='onchange')
    date = fields.Date(string='Date',readonly=True ,default=fields.Date.today(),track_visibility='onchange')
    case_stages_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")


class CaseSubCategory(models.Model):
    _name = 'case.sub.categories'
    _inherit = ['mail.thread']

    name = fields.Char(string='Sub Categories',required=True,track_visibility='onchange')