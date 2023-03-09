# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class InheritResUsers(models.Model):
    _inherit = 'res.users'

    user_type = fields.Selection(
        [
        ('client', 'Client'),
        ('organisation', 'Organisation'),
        ('lawyer', 'Lawyer'),
        ('claimant_plaintiff_lawyer', 'Claimant/Plaintiff Lawyer'),
        ('judge', 'Judge'),
        ('registrar', 'Registrar'),
        ('witness', 'Witness'),
        ('claimant_plaintiff', 'Claimant/Plaintiff'),
        ('court_admin', 'Court Admin'),
        ('case_clerk', 'Court Clerk'),
        ], string='User Type', track_visibility='onchange')


class ResCompany(models.Model):
    _inherit = "res.company"

    client_seq = fields.Many2one('ir.sequence', string="Client Seq")
    lawyer_seq = fields.Many2one('ir.sequence', string="Lawyer Seq")
    claimant_plaintiff_lawyer_seq = fields.Many2one('ir.sequence', string="Claimant/Plaintiff Lawyer Seq")
    judge_seq = fields.Many2one('ir.sequence', string="Judge Seq")
    witness_seq = fields.Many2one('ir.sequence', string="Witness Seq")
    claimant_plaintiff_seq = fields.Many2one('ir.sequence', string="Claimant/Plaintiff Seq")
    court_seq = fields.Many2one('ir.sequence', string="Court Seq")
    registrar_seq = fields.Many2one('ir.sequence', string="Registrar Seq")
    court_admin_seq = fields.Many2one('ir.sequence', string="Registrar Seq")
    registry_clerk_seq = fields.Many2one('ir.sequence', string="Court Clerk Seq")