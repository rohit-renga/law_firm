# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class ActAct(models.Model):
    _name = 'act.act'
    _rec_name = 'act_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Act'

    act_seq  = fields.Char(
        size=256, string='ACT Seq', readonly=True, default='New ACT', copy=False)
    act_name = fields.Many2one('act.act.name',string='Act Name',track_visibility='onchange')
    act_no = fields.Char(string='Act No',track_visibility='onchange')
    act_type = fields.Selection(
        [('criminal', 'Criminal'), ('civil', 'Civil')], string='Act Type',track_visibility='onchange')
    act_link = fields.Char(string='Link',track_visibility='onchange')
    act_year = fields.Char(string='Act Year',track_visibility='onchange')
    act_desc = fields.Html(string='Act Description',track_visibility='onchange')
    act_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")


    @api.model
    def create(self, values):
        if values.get('act_name', ''):
            values['act_seq'] = self.env['ir.sequence'].next_by_code('act.act') or ''
        res = super(ActAct, self).create(values)
        return res


class ActActName(models.Model):
    _name = 'act.act.name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',required=False)

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Act Name Must Be Unique!!!')]