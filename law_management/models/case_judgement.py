# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class CaseJudgement(models.Model):
    _name = 'case.trail.judgement'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _rec_name = 'judgement_seq'
    _description = 'Judgement'

    judgement_seq = fields.Char(
        size=256, string='Judgement Seq', readonly=True, default='Judgement', copy=False)
    case = fields.Many2one('matter.matter', string='Case Number',
                           track_visibility='onchange', required=True)
    judgement_case_name = fields.Char(related='case.case_name', string='Case Name')
    client_name = fields.Many2one('client.client', string='Client Name', track_visibility='onchange')
    judgement_date = fields.Date(
        'Judgement Date', default=fields.Date.today(), readonly=True)
    judgement_description = fields.Text(
        string='Judgement', track_visibility='onchange', required=True)
    judgement_category_id = fields.Many2one('case.judgement.category', string="Judgement Catrgoty")
    type = fields.Selection([('civil', 'Civil')], string="Judgement Parent Category", required=True, default='civil')
    category_id = fields.Many2one('case.judgement.category', string='Sub Category', track_visibility='onchange')
    law_code = fields.Many2one(
        'law.code', string='Law Code', track_visibility='onchange')
    accused = fields.Many2one('accuse.details',string="Claimant/Plaintiff")
    reference_evidence_ids = fields.One2many(
        'case.trail.reference.evidence', 'reference_evidence_id', string='Reference')
    attachment_id = fields.Many2many(
        'ir.attachment', string='Attachments', track_visibility='onchange')
    trail_judgement_id = fields.Many2one(
        'case.trail', string='Trial Name', track_visibility='onchange')
    judgement_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    evidence_count = fields.Float(
        compute="_compute_evidence_count", string='Evidence')
    judgement_count = fields.Float(
        compute="_compute_judgement_count", string='Judgement')
    judgement_document_ids = fields.One2many('case.judgement.document','judgement_document_id',string="Document")
    law_code_ids = fields.One2many('law.code','judgement_law_code_id')
    client_ids = fields.Many2many(related='case.client_name_many')
    accuse_ids = fields.Many2many(related='case.accuse_ids')

    @api.model
    def create(self, values):
        if values.get('judgement_seq', 'Judgement') == 'Judgement':
            values['judgement_seq'] = self.env['ir.sequence'].next_by_code(
                'case.trail.judgement') or 'Judgement'
        res = super(CaseJudgement, self).create(values)
        return res

    @api.onchange('case')
    def _onchange_accuse_id(self):
        domain = {}
        item_ids_list = []
        for item in self.case.client_name_many:
            item_ids_list.append(item.id)
        domain = {'client_name':[('id', 'in', item_ids_list)]}
        return {'domain': domain }

    @api.onchange('case')
    def _onchange_accused(self):
        domain = {}
        items_list = []
        for item in self.case.accuse_ids:
            items_list.append(item.id)
        domain = {'accused': [('id', 'in', items_list)]} 
        return {'domain': domain}

    
    @api.multi
    def _compute_judgement_count(self):
        for Doc in self:
            Doc.judgement_count = len(Doc.judgement_document_ids)

    @api.multi
    def case_judgement_document(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.judgement_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('judgement_document_id','in', [self.id])]
            action['context'] = ({'default_judgement_document_id': self.id or False,
                                  })
            return action

    @api.multi
    def _compute_evidence_count(self):
        self.evidence_count = self.env['case.trail.evidance'].search([]).search_count(
                [('admissible_evidance', '=', True),('evidance_case', '=', self.case.id)])


    @api.multi
    def action_accuse_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.accuse_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_document_id', 'in', [self.id])]
            action['context'] = ({'default_accuse_document_id': self.id})
            return action


    @api.multi
    def action_case_trail_judgement(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.case_trail_evidance_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('evidance_case', 'in', [self.case.id])]
            action['context'] = ({'default_judgement_id': self.id})
            return action
       
     
class CaseTrailReferenceEvidence(models.Model):
    _name = 'case.trail.reference.evidence'
    _order = 'create_date desc'
    _rec_name = 'trail_name'
    
    trail_name = fields.Many2one('matter.matter',string='Case Name',track_visibility='onchange')
    reference_evidence = fields.Many2one('case.trail.evidance.name',string='Evidence',domain=[('value', '=', True)])
    case = fields.Char(string='Case',track_visibility='onchange')
    lawyer = fields.Many2one('lawyer.details',string='Lawyer',track_visibility='onchange')
    opposition_lawyer = fields.Many2one('opposition.lawyer',string='Claimant/Plaintiff Lawyer',track_visibility='onchange')
    reference_evidence_id = fields.Many2one('case.trail.judgement',string='Judgement',track_visibility='onchange')

class CaseJudgementDocument(models.Model):
    _name = 'case.judgement.document'
    _order = 'create_date desc'
    _rec_name = 'doc_name'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.', track_visibility='onchange')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    jdg_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    judgement_document_id = fields.Many2one('case.trail.judgement',string='Judgement')    

class JudgementCategory(models.Model):
    _name = 'case.judgement.category'
    _rec_name = 'name'
    _order = 'create_date desc'

    type = fields.Selection(
        [('civil', 'Civil')], default='civil' , string='Parent Category')
    name = fields.Many2one('judgement.sub.categories',string='Child Category')

class JudgementSubCategory(models.Model):
    _name = 'judgement.sub.categories'
    _rec_name = 'j_sub_category'

    j_sub_category = fields.Char(string='Judgement Sub Categories',required=True)
