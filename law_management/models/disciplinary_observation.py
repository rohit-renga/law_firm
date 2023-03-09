# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class CaseDisciplinary(models.Model):
    _name = 'case.discipline'
    _rec_name = 'do_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Discipline'

    case_do_id = fields.Many2one('matter.matter',string='Case Number',required=True)
    discipline_case_name = fields.Char(related='case_do_id.case_name', string='Case Name')
    discipline_observation_seq = fields.Char(
        size=256, string='Discipline Observation Seq', readonly=True, default='New Discipline Observation', copy=False)
    misconduct_by = fields.Selection([('client','Client'),('accuse','Claimant / Plaintiff')],string="Misconduct By",track_visibility='onchange',required=True)
    client_id = fields.Many2one('client.client',string="Client")
    accuse_id = fields.Many2one('accuse.details',string="Claimant / Plaintiff")
    do_name = fields.Char(string='Name',track_visibility='onchange',required=True)
    do_date = fields.Date(string='Date',default=fields.Date.today(),track_visibility='onchange')
    do_desc = fields.Text(string='Description',track_visibility='onchange')

