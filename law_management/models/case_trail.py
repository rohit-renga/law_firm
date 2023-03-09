# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import math


class CaseTrail(models.Model):
    _name = 'case.trail'
    _rec_name = 'trail_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Trial'

    matter_id = fields.Char(string='Case ID')
    matter_name = fields.Many2one('matter.matter', string='Case Number',track_visibility='onchange')
    t_case_name = fields.Char(related='matter_name.case_name', string='Case Name')
    client_name = fields.Many2one(
        'client.client',related='matter_name.client_name', string='Client Name', track_visibility='onchange')
    accuse_name = fields.Many2one('accuse.details',related='matter_name.accused',string='Claimant / Plaintiff')
    client_ids = fields.Many2many(
        'client.client',string='Client Name', related='matter_name.client_name_many', track_visibility='onchange')
    accuse_ids = fields.Many2many('accuse.details', related='matter_name.accuse_ids', string='Claimant / Plaintiff')
    trail_name = fields.Char(string='Trial Name', required=True,track_visibility='onchange')
    trail_date = fields.Date(string='Trial Date',default=fields.Date.today() ,required=True,track_visibility='onchange')
    court_name = fields.Many2one('court.court',related='matter_name.court_id', string='Court', required=True,track_visibility='onchange')
    court_roomno = fields.Char(string='Court Room No.',track_visibility='onchange')
    judge_name = fields.Many2one(
        'judge.details',related='matter_name.judge_id', string='Judge', required=True,track_visibility='onchange')
    lawyer_name = fields.Many2one(
        'lawyer.details',related='matter_name.assign_id', string='Lawyer', required=True,track_visibility='onchange')
    opposition_lawyer_name = fields.Many2one(
        'opposition.lawyer',related='matter_name.opp_lawyer_id', string='Claimant/Plaintiff Lawyer',track_visibility='onchange')
    trail_description = fields.Text(string='Description',track_visibility='onchange')
    trail_judgement = fields.Text(String='Judgement',track_visibility='onchange')
    trail_document_ids = fields.One2many(
        'case.trail.document', 'trail_document_id', string='Documents')
    trail_judgement_ids = fields.One2many(
        'case.trail.judgement', 'trail_judgement_id', string='Judgement')
    trail_evidance_ids = fields.One2many(
        'case.trail.evidance', 'trail_evidance_id', string='Evidence')
    judgement_count = fields.Integer(
        compute="_compute_judgement_count", string='Trials',track_visibility='onchange')
    evidance_count = fields.Integer(
        compute="_compute_evidance_count", string='Trials')
    ctrail_d_count = fields.Integer(
        compute="_compute_ctrail_d_count", string='Document')
    trail_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    
    #Button
    @api.multi
    def case_trail_judgement(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.case_trail_judgement_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('trail_judgement_id', '=', self.id)]
            action['context'] = ({
                                  'default_case': self.matter_name.id,
                                  'default_trail_judgement_id':self.id,

                    })
            return action

    @api.multi
    def case_trail_evidence(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.case_trail_evidance_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('trail_evidance_id', '=', self.id)]
            action['context'] = ({'default_trail_evidance_id': self.id,
                                  'default_evidance_lawyer': self.lawyer_name.id,
                                  'default_evidance_opposition_lawyer': self.opposition_lawyer_name.id,
                                  'default_evidance_case': self.matter_name.id,

                    })
            return action

    @api.multi
    def case_trail_document(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.trail_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('trail_document_id','in', [self.id])]
            action['context'] = ({'default_trail_document_id': self.id or False,
                                  })
            return action

    #Count
    @api.multi
    def _compute_judgement_count(self):
        JudgementCount = self.env['case.trail.judgement']
        for judgement in self:
            judgement.judgement_count = JudgementCount.search_count(
                [('trail_judgement_id', '=', judgement.id)])

    @api.multi
    def _compute_evidance_count(self):
        EvidanceCount = self.env['case.trail.evidance']
        for evidance in self:
            evidance.evidance_count = EvidanceCount.search_count(
                [('trail_evidance_id', '=', evidance.id)])

    @api.multi
    def _compute_ctrail_d_count(self):
        DocumentCount = self.env['case.trail.document']
        for Doc in self:
            Doc.ctrail_d_count = DocumentCount.search_count(
                [('trail_document_id', '=', Doc.id)])

class TrailName(models.Model):
    _name = 'trail.name'
    _order = 'create_date desc'

    name = fields.Char(string='Name',required=True,track_visibility='onchange')


class CaseTrailDocument(models.Model):
    _name = 'case.trail.document'
    _order = 'create_date desc'
    _rec_name = 'doc_name'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    trd_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    trail_document_id = fields.Many2one('case.trail',string='Trial')
