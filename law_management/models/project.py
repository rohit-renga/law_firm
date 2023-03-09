# coding: utf-8

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta

class Project(models.Model):
    _inherit = 'project.project'

    case_id = fields.Many2one("matter.matter", string="Case")
    lawyer_id = fields.Many2one("lawyer.details", string="Lawyer")
    

class ProjectTask(models.Model):
    _inherit = 'project.task'

    case_id = fields.Many2one("matter.matter", string="Case")
    assign_to = fields.Selection([('lawyer','Lawyer'),('judge','Judge'),('court_admin','Court Admin'),('registry_clerk','Court Clerk')],string="Assign To")
    lawyer = fields.Many2one("lawyer.details", string="Lawyer")
    judge  = fields.Many2one("judge.details", string="Judge")
    court_admin = fields.Many2one("court.admin", string="Court Admin")
    registry_clerk = fields.Many2one("case.clerk", string=" Court Clerk")
    start_date = fields.Date(string="Start date")
    case_task_id = fields.Many2one('matter.matter',string='Task')

    @api.model
    def send_task_secheduler_email_lawyer(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'send_task_secheduler_email_lawyer')[1]
        record = temp_obj.browse(trail_template_id)
        date_before_deadline = date.today() + timedelta(days=1)
        date_3 = str(date_before_deadline)
        obj = self.env['project.task'].search([])
        template = self.env.ref(
            'law_management.send_task_secheduler_email_lawyer')
        for task in obj:
            if task.date_deadline:
                dates_1 = str(task.date_deadline)
                date_2 = str(dates_1)
                if date_3 == date_2:
                    record.send_mail(task.id, force_send=True)

    @api.model
    def send_id_of_assign_person(self):
        if self.lawyer:
            return self.lawyer.lawyer_emailW
        elif self.judge:
            return self.judge.judge_emailW
        elif self.court_admin:
            return self.court_admin.admin_email
        else:
            return self.registry_clerk.clerk_email

    @api.model
    def send_person_name(self):
        if self.lawyer:
            return self.lawyer.lawyer_name
        elif self.judge:
            return self.judge.judge_name
        elif self.court_admin:
            return self.court_admin.court_admin_name
        else:
            return self.registry_clerk.case_clerk_name