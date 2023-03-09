# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class LawCodeNo(models.Model):
    _name = 'law.code.no'
    _order = 'create_date asc'
    _description = 'Law Code'
    

    name = fields.Char(string='Code No.',required=True,track_visibility='onchange')
    short_description = fields.Char(string="Short Description",required=True)
    
    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Law Code No. Must Be Unique!')]
    

class LawCode(models.Model):
    _name = 'law.code'
    _rec_name = 'code_number'
    _order = 'code_number asc'
    _inherit = ['mail.thread']

    
    code_number = fields.Many2one(
        'law.code.no', string='Code Number',track_visibility='onchange')
    is_obselete = fields.Boolean(string='Is Obselete',track_visibility='onchange')
    short_des = fields.Char(related="code_number.short_description",string="Short Description")
    year_in_place = fields.Date(string="Year in Place", track_visibility='onchange')
    ammendment_law_code = fields.Many2one('law.code', string='Ammendent Law Code',track_visibility='onchange')
    obselete_law_code = fields.Many2one('law.code',string='Obselete Law Code',track_visibility='onchange')
    desciption = fields.Html(string='Description',track_visibility='onchange')
    law_article_no = fields.Char(string='Article No',track_visibility='onchange')
    law_art_link = fields.Char(string='Link',track_visibility='onchange')
    law_art_name = fields.Char(string='Article Name',track_visibility='onchange')
    law_art_category = fields.Selection(
        [('criminal', 'Criminal'), ('civil', 'Civil')], string='Type',track_visibility='onchange')
    law_art_notes = fields.Html(string='Article Description')
    article = fields.Integer(compute="_compute_articles")
    
    law_code_document_ids = fields.One2many(
        'law.code.document', 'law_code_document_id', string='Document')
    lc_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    lc_doc_count = fields.Integer(
        compute="_compute_lcdoc_count", string='Document')
    articles_id = fields.One2many('article.article', 'article_id', string="Articles")
    judgement_law_code_id = fields.Many2one('case.trail.judgement',string='Judgement')

    
    @api.multi
    def _compute_articles(self):
        articletLine = self.env['article.article']
        for cno in self:
            cno.article = articletLine.search_count(
                [('article_id', '=', cno.id)])

    @api.multi
    def _compute_lcdoc_count(self):
        DocLine = self.env['law.code.document']
        for doc in self:
            doc.lc_doc_count = DocLine.search_count(
                [('law_code_document_id', '=', doc.id)])

    @api.multi
    def action_articles_view(self):
        return {
            'name': _('Articles'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'article.article',
            'type': 'ir.actions.act_window',
            'domain': [('article_id', '=', self.id)],
            'context': {
                'default_article_id': self.id,
                'default_code_number': self.code_number.id,
                'tree_view_ref': self.env.ref('law_management.view_article_article_tree'),
                'form_view_ref': self.env.ref('law_management.view_article_article_form')},
        }

    @api.multi
    def action_law_code_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.law_code_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('law_code_document_id', 'in', [self.id])]
            action['context'] = ({'default_law_code_document_id': self.id})
            return action

class LawCodeDocument(models.Model):
    _name = 'law.code.document'
    _rec_name = 'doc_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments',track_visibility='onchange')
    comment = fields.Text(string='Description',track_visibility='onchange')
    date = fields.Date(string='Date')
    lcd_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    law_code_document_id = fields.Many2one(
        'law.code', string='Law Code')
