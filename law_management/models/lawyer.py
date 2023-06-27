# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class LawyerDetails(models.Model):
    _name = 'lawyer.details'
    _rec_name = 'lawyer_name'
    _description = 'Lawyer'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _inherits = {
        'res.users': 'user_id',
    }

    user_id = fields.Many2one(
    'res.users', string='Related User', required=False,
    ondelete='cascade', help='User-related data of the Lawyer',store=True)
    lawyer_id = fields.Char(string='Lawyer ID')
    image = fields.Binary(string='Image', attachment=True)
    lawyer_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=False)
    lawyer_mobileP = fields.Char(string='Mobile', track_visibility='onchange')
    lawyer_emailP = fields.Char(
        string='Email(Personal)', track_visibility='onchange')
    lawyer_emailW = fields.Char(
        string='Email', track_visibility='onchange')
    lawyer_nationality = fields.Many2one('nationality.master', string='Nationality', ondelete='restrict', track_visibility='onchange')
    lawyer_nationality_code = fields.Char(related='lawyer_nationality.nationality_code',string='Nationality Code')
    lawyer_account = fields.Integer(
        compute="_compute_lawyer_account_count", string='Account')
    total_cases = fields.Integer(
        compute="_compute_total_cases_count", string='Total Cases')
    won_cases = fields.Integer(
        compute="_compute_won_cases_count", string='Won Cases')
    lost_cases = fields.Integer(
        compute="_compute_lost_cases_count", string='Lost Cases')
    settlement_cases = fields.Integer(
        compute="_compute_settlement_cases_count", string='Settlement Cases')
    # ongoing_cases = fields.Integer(
    #     compute="_compute_ongoing_cases_count", string='Ongoing Cases')
    active = fields.Boolean(
        default=True, help="The active field allows you to hide the category without removing it.")
    invoiced = fields.Integer(
        compute="_compute_invoiced_count", string='Invoices')
    expenses = fields.Integer(
        compute="_compute_expenses_count", string='Expenses')
    lawyer_account_details_ids = fields.One2many(
        'account.master', 'lawyer_account', string='Account')
    lawyer_doc_ids = fields.One2many(
        'lawyer.document', 'lawyer_document_id', string='Documents')
    l_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    l_doc_count = fields.Integer(
        compute="_compute_ldoc_count", string='Document')
    ongoing_case_ids = fields.One2many(
        'matter.matter', 'assign_id', string='Cases ongoing', domain=lambda self: [('case_result','=','cases_on_going')])
    won_case_ids = fields.One2many(
        'matter.matter', 'assign_id', string='Cases won', domain=lambda self: [('case_result','=','won')])
    lost_case_ids = fields.One2many(
        'matter.matter', 'assign_id', string='Cases lost', domain=lambda self: [('case_result','=','lost')])
    settlement_case_ids = fields.One2many(
        'matter.matter', 'assign_id', string='Cases settled', domain=lambda self: [('case_result','=','settlement')])


    @api.model
    def create(self, values):
        if values.get('lawyer_name', ''):
            values['lawyer_id'] = self.env['ir.sequence'].next_by_code('lawyer.details') or ''
            name = values.get('lawyer_name', '')
            values['name'] = name
            login = values.get('lawyer_emailW', '')
            if login:
                values['login'] = login
            values['user_type'] = 'lawyer'
        res = super(LawyerDetails, self).create(values)
        if res.lawyer_mobileP:
            mobile1 = res.lawyer_mobileP
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        values['groups_id'] = []
        group_user = self.env.ref('law_management.group_law_firm_user_lawyer')
        res.sudo().write({'groups_id': [(6, 0, [group_user.id])]})
        return res

    @api.multi
    def write(self, values):
        if values.get('lawyer_mobileP', ''):
            mobile1 = values.get('lawyer_mobileP', '')
            if mobile1.isdigit():
                pass
            else:
                raise ValidationError(_('Enter Only Numerical Value in Mobile No.'))
        return super(LawyerDetails, self).write(values)


    #Button
    @api.multi
    def lawyer_account_view_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('lawyer_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'lawyer',
                                  'default_lawyer_account': self.id or False})
            return action

    #Count    
    @api.multi
    def _compute_ldoc_count(self):
        DocLine = self.env['lawyer.document']
        for doc in self:
            doc.l_doc_count = DocLine.search_count(
                [('lawyer_document_id', '=', doc.id)])

    @api.multi
    def _compute_lawyer_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.lawyer_account = accountLine.search_count(
                [('lawyer_account', '=', partner.id)])

    @api.multi
    def _compute_invoiced_count(self):
        account = self.env['account.invoice']
        for partner in self:
            partner.invoiced = account.search_count(
                [('partner_id', '=', partner.id)])

    @api.multi
    def _compute_expenses_count(self):
        for rec in self:
            expense_data = self.env['hr.expense'].search(
                [('lawyer_id', '=', self.id)])
            if expense_data:
                rec.expenses = len(expense_data)

    # @api.multi
    # def _compute_total_cases_count(self):
    #     cases = self.env['matter.matter']
    #     for partner in self:
    #         partner.total_cases = cases.search_count(
    #             [('assign_id', '=', partner.id)])

    # @api.multi
    # def _compute_won_cases_count(self):
    #     pass

    # @api.multi
    # def _compute_lost_cases_count(self):
    #     pass

    # @api.multi
    # def _compute_settlement_cases_count(self):
    #     pass

    # @api.multi
    # def _compute_ongoing_cases_count(self):
    #     cases = self.env['matter.matter']
    #     for lawyer in self:
    #         lawyer.ongoing_cases = cases.search_count(
    #             [('assign_id', '=', lawyer.id),('case_result','=','cases_on_going')])

    @api.multi
    def action_lawyer_invoices(self):
        return {
            'name': _('Customer Invoices'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id,
                        'tree_view_ref': self.env.ref('account.invoice_tree'),
                        'form_view_ref': self.env.ref('account.invoice_form')},
        }

    @api.multi
    def action_lawyer_expenses(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'hr_expense.hr_expense_actions_my_unsubmitted')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('lawyer_id', 'in', [self.id])]
            action['context'] = ({'default_lawyer_id': self.id})
            return action

    
    @api.multi
    def action_lawyer_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.lawyer_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('lawyer_document_id', 'in', [self.id])]
            action['context'] = ({'default_lawyer_document_id': self.id})
            return action

    # @api.multi
    # def action_total_cases_view(self):
    #     return {
    #         'name': _('Total Cases'),
    #         'view_type': 'form',
    #         'view_mode': 'tree,form',
    #         'res_model': 'matter.matter',
    #         'type': 'ir.actions.act_window',
    #         'domain': [('assign_id', '=', self.id)],
    #         'context': {'default_assign_id': self.id,
    #                     'tree_view_ref': self.env.ref('law_management.view_matter_matter_tree'),
    #                     'form_view_ref': self.env.ref('law_management.view_matter_matter_form')},
    #     }

    # @api.multi
    # def action_won_cases_view(self):
    #     pass

    # @api.multi
    # def action_lost_cases_view(self):
    #     pass

    # @api.multi
    # def action_settlement_cases_view(self):
    #     pass

    @api.multi
    def action_ongoing_cases_view(self):
        return {
            'name': _('Ongoing Cases'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'matter.matter',
            'type': 'ir.actions.act_window',
            'domain': [('assign_id', '=', self.id),('case_result','=','cases_on_going')],
            'context': {'default_assign_id': self.id,
                        'tree_view_ref': self.env.ref('law_management.view_matter_matter_tree'),
                        'form_view_ref': self.env.ref('law_management.view_matter_matter_form')},
        }


class LawyerDocument(models.Model):
    _name = 'lawyer.document'
    _rec_name = 'lawyer_document_id'
    _order = 'create_date desc'
    
    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description')
    date = fields.Date(string='Date')
    ld_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    lawyer_document_id = fields.Many2one(
        'lawyer.details', string='Lawyer')
    category_id = fields.Many2one('document.category')
