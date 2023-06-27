# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time


class CaseCharges(models.Model):
    _name = 'case.charge'
    _rec_name = 'case_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Case Charge'


    case_name = fields.Many2one("matter.matter", string="Case Number",
        track_visibility='onchange')
    charges_case_name = fields.Char(related='case_name.case_name', string='Case Name')
    client_name = fields.Many2one('client.client',string='Client', track_visibility='onchange')
    accuse_name = fields.Many2one('accuse.details',string="Claimant")
    number = fields.Many2one("law.code", string="Law Code",
        track_visibility='onchange')
    date = fields.Date(string="Date",default=fields.Date.today(),
        track_visibility='onchange')
    amount = fields.Float(sting='Amount',track_visibility='onchange')
    desciption = fields.Html("Description",track_visibility='onchange')
    case_charges_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user,
        readonly="True")
    client_ids = fields.Many2many(related='case_name.client_name_many')
    accuse_ids = fields.Many2many(related='case_name.accuse_ids')
    laws_desc = fields.Char(related="number.short_des")

    api.onchange('case_name')
    def _onchange_client_name(self):
        domain = {}
        item_ids_list = []
        for item in self.case_name.client_name_many:
            item_ids_list.append(item.id)
        domain = {'client_name':[('id', 'in', item_ids_list)]}
        return {'domain': domain }

    @api.onchange('case_name')
    def _onchange_accuse_name(self):
        domain = {}
        items_list = []
        for item in self.case_name.accuse_ids:
            items_list.append(item.id)
        domain = {'accuse_name': [('id', 'in', items_list)]} 
        return {'domain': domain}
