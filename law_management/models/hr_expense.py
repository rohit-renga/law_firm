# coding: utf-8

from odoo import models, fields, api

class HrExpense(models.Model):
    _inherit = "hr.expense"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=False, readonly=False, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1))
    case_expense_id = fields.Many2one("matter.matter", string="Case Number")
    lawyer_id = fields.Many2one("lawyer.details")
    exp_case_name = fields.Char(related='case_expense_id.case_name', string="Case Name")