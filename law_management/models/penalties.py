# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class penaltiesForm(models.Model):
    _name = "penalties.form"
    _rec_name = "penalties_name"
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Penalties'

    penalties_name = fields.Char(string='Name',track_visibility='onchange')
    penalties_case_name =fields.Char(related='matter_id.case_name', string='Case Name')
    matter_id = fields.Many2one('matter.matter', string='Case Number',track_visibility='onchange')
    case_id = fields.Char(related="matter_id.caseid",
                          string='Case ID')
    submitted_by = fields.Selection([('client','Client'),('accuse','Claimant / Plaintiff'),('lawyer', 'Lawyer'),('judge', 'Judge')],string="Submitted By",required=True)
    client_name_id = fields.Many2one('client.client', 'Client', 
                                     ondelete="cascade", track_visibility='onchange')
    accuse_name_id = fields.Many2one(
        'accuse.details', string='Claimant / Plaintiff',track_visibility='onchange')
    judge_name_id = fields.Many2one('judge.details')
    lawyer_name_id = fields.Many2one('lawyer.details')
    # client_invisible_id = fields.Many2many('matter.matter', related='matter_id.client_name_many')
    receipt_number = fields.Char("Receipt number",track_visibility='onchange')
    penalty_amount = fields.Float("Amount",track_visibility='onchange')
    reason_for_penalty = fields.Char("Reason",track_visibility='onchange')
    check_for_paid = fields.Boolean(string='Is Paid',track_visibility='onchange')
    date = fields.Date(string='Date',track_visibility='onchange',default=fields.Date.today(),readonly=True)
    date_of_payment = fields.Date(string='Date of Payment',track_visibility='onchange')
    penalty_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    @api.onchange('matter_id')
    def _onchange_client_id(self):
        domain = {}
        client_list = []
        for client in self.matter_id.client_name_many:
            client_list.append(client.id)
        domain = { 'client_name_id': [ ('id', 'in', client_list) ] } 
        return { 'domain': domain }

    @api.onchange('matter_id')
    def _onchange_accuse_id(self):
        domain = {}
        accuse_list = []
        for accuse in self.matter_id.accuse_ids:
            accuse_list.append(accuse.id)
        domain = { 'accuse_name_id': [ ('id', 'in', accuse_list) ] } 
        return { 'domain': domain }




