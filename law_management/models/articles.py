# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time


class ArticleArticle(models.Model):
    _name = 'article.article'
    _rec_name = 'article_no'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Article'

    article_seq  = fields.Char(
        size=256, string='Article Seq', readonly=True, default='New Article', copy=False)
    article_no = fields.Char(string='Article No',track_visibility='onchange')
    code_number = fields.Many2one(
        'law.code.no', string="Code Number",track_visibility='onchange')
    art_link = fields.Char(string='Link',track_visibility='onchange')
    art_name = fields.Many2one('art.art.name',string='Article Name',track_visibility='onchange')
    art_category = fields.Selection(
        [('criminal', 'Criminal'), ('civil', 'Civil')], string='Type',track_visibility='onchange')
    art_notes = fields.Html(string='Article Description',track_visibility='onchange')
    article_id = fields.Many2one('law.code',track_visibility='onchange') 
    article_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    @api.model
    def create(self, values):
        if values.get('art_name', ''):
            values['article_seq'] = self.env['ir.sequence'].next_by_code('article.article') or ''
        res = super(ArticleArticle, self).create(values)
        return res


class ArtArtName(models.Model):
    _name = 'art.art.name'
    _order = 'create_date desc'

    name = fields.Char(string='Name',required=False,track_visibility='onchange')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Act Name Must Be Unique!!!')]