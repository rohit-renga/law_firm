# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class CaseEvidance(models.Model):
    _name = 'case.trail.evidance'
    _rec_name = 'evidance_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Evidence'

    judgment_id = fields.Many2one('case.trail.judgement')
    evidance_case = fields.Many2one('matter.matter', string='Case Number')
    evidence_case_name = fields.Char(related='evidance_case.case_name', string='Case Name')
    client_name = fields.Many2one('client.client',string='Name', track_visibility='onchange')
    evidance_description = fields.Text(string='Evidence Description',track_visibility='onchange')
    evidance_name = fields.Many2one('case.trail.evidance.name', string='Evidence',required=False,track_visibility='onchange')
    evidance_lawyer = fields.Many2one('lawyer.details',related='evidance_case.assign_id', string='Lawyer',track_visibility='onchange')
    evidance_opposition_lawyer = fields.Many2one(
        'opposition.lawyer',related='evidance_case.opp_lawyer_id', string='Claimant/Plaintiff Lawyer',track_visibility='onchange')
    admissible_evidance = fields.Boolean(string='Admissible Evidence',track_visibility='onchange')
    evidance_ids = fields.One2many(
        'evidance.details', 'evidance_id', string='Evidence',track_visibility='onchange')
    trail_evidance_id = fields.Many2one('case.trail',string='Trial Name')
    evidance_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    evidence_document_defendant_ids = fields.One2many('case.evidence.document.defendant','evidence_document_id',string="Defendant")
    evidence_document_claimant_ids = fields.One2many('case.evidence.document.claimant','evidence_document_id',string="Claimant")
    evidence_count_defendant = fields.Integer(
        compute="_compute_evidence_count_defendant", string='Evidence',track_visibility='onchange')
    evidence_count_claimant = fields.Integer(
        compute="_compute_evidence_count_claimant", string='Evidence',track_visibility='onchange')
    lawyer_visible = fields.Selection([('lawyer', 'Lawyer'), ('opposition', 'Claimant/Plaintiff Lawyer')], string="Evidence By")

    @api.model
    def default_get(self, default_fields):
        res = super(CaseEvidance, self).default_get(default_fields)
        if 'judgment_id' in default_fields:
            res.update({'judgment_id': self._context.get('judgement_id', False)})
        return res

    @api.model
    def create(self, values):
        res = super(CaseEvidance, self).create(values)
        if res.admissible_evidance:
            if res.evidance_name:
                res.evidance_name.write({'value':True})
        return res

    @api.multi
    def write(self, values):
        res = super(CaseEvidance, self).write(values)
        if self.evidance_name:
            self.evidance_name.write({'value':self.admissible_evidance})
        return res

    @api.multi
    def _compute_evidence_count_defendant(self):
        for doc in self:
            doc.evidence_count_defendant = len(doc.evidence_document_defendant_ids)

    @api.multi
    def _compute_evidence_count_claimant(self):
        for doc in self:
            doc.evidence_count_claimant = len(doc.evidence_document_claimant_ids)

    @api.multi
    def case_evidence_document_defendant(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.case_evidence_document_defendant_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('evidence_document_id','in', [self.id])]
            action['context'] = ({'default_evidence_document_id': self.id or False,})
        return action


    @api.multi
    def case_evidence_document_claimant(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.case_evidence_document_claimant_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('evidence_document_id','in', [self.id])]
            action['context'] = ({'default_evidence_document_id': self.id or False,
                                  })
        return action


class EvidanceDetails(models.Model):
    _name = 'evidance.details'
    _rec_name = 'name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',track_visibility='onchange') 
    description = fields.Text(string='Description',track_visibility='onchange')
    tags = fields.Char(string='Tags',track_visibility='onchange')
    attachment_id = fields.Many2many('ir.attachment', string='Attachments',track_visibility='onchange')
    evidance_id = fields.Many2one('case.trail.evidance',string='Evidence',track_visibility='onchange')
    # attachment

class CaseTrailEvidanceName(models.Model):
    _name = 'case.trail.evidance.name'
    _rec_name = 'name'
    _order = 'create_date desc'
    

    name = fields.Char(string='Name',track_visibility='onchange', required=False)
    value = fields.Boolean(string='True',track_visibility='onchange')

class CaseEvidenceDocument(models.Model):
    _name = 'case.evidence.document.claimant'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _rec_name = 'doc_name'

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    evi_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    evidence_document_id = fields.Many2one('case.trail.evidance',string='Evidence')

class CaseEvidenceDocument(models.Model):
    _name = 'case.evidence.document.defendant'
    _order = 'create_date desc'
    _rec_name = 'doc_name'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    evi_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    evidence_document_id = fields.Many2one('case.trail.evidance',string='Evidence')    
