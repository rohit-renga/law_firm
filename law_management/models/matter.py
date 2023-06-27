# coding: utf-8

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import re


class MatterMatter(models.Model):
    _name = 'matter.matter'
    _rec_name = 'matter_seq'
    _description = 'Case'
    _order = 'matter_seq asc'
    _order = 'case_result asc'
    _inherit = ['mail.thread']

    def _get_default_stages(self):
        ids = self.env['case.stages'].search([
            ('case_defalut_stage', '=', True)])
        return ids

    matter_seq = fields.Char(
        size=256, string='Matter Seq', readonly=True, default='Case ID', copy=False)
    court_category = fields.Many2one('court.category',string="Court Category")
    caseid = fields.Char("Cause ID", required=False)
    cause_name = fields.Char("Cause Name", required=False)
    case_name = fields.Char(string='Case Name')
    type = fields.Selection(
        [('civil', 'Civil')],default='civil' ,required=False, string='Parent Category')
    description = fields.Html(string='Description')
    # description_text = fields.Text(string='Description', compute="get_text_discription")
    case_doc_ids = fields.One2many(
        'matter.doc', 'case_doc_id', string='Document')
    case_history_ids = fields.One2many(
        'case.history', 'case_history_id', string='History')
    stage_id = fields.Many2one(
        'case.stages', string='Stage', default=_get_default_stages, track_visibility='onchange')
    matter_state_id = fields.Many2one('res.country.state', string='State')
    priority = fields.Many2one('case.priority', string="Case Priority")
    court_id = fields.Many2one('court.court', string="Court")
    date = fields.Date(string='Current Date', default=fields.Date.today())
    user = fields.Many2one('res.users', string="Created By",
                           default=lambda self: self.env.user, readonly="True")
    color = fields.Integer(string='Color Index')
    category_id = fields.Many2one(
        'case.category', string='Sub Category')
    client_name = fields.Many2one('client.client', string='Client')
    client_name_many = fields.Many2many('client.client', "matter_client_rel", "matter_id", "client_id", string='Client')
    accused = fields.Many2one('accuse.details', string='Claimant/Plaintiff')
    accuse_ids = fields.Many2many('accuse.details', string='Claimant/Plaintiff')
    assign_id = fields.Many2one('lawyer.details', string='Lawyer')
    opp_lawyer_id = fields.Many2one('opposition.lawyer', string='Claimant/Plaintiff Lawyer')
    judge_id = fields.Many2one('judge.details', string='Judge')
    pay_type = fields.Selection([('pay_per_hour', 'By Hour'), (
        'pay_per_trial', 'By Trial'), ('pay_per_fixed', 'By Fixed')], string='Payment Type')
    project_id = fields.Many2one("project.project", string="Project")
    # Date
    date_open = fields.Date(string='Opened Date', track_visibility='onchange')
    date_close = fields.Date(string='Closed Date', track_visibility='onchange')
    reopen_date = fields.Date(string='Reopen Date',
                              track_visibility='onchange')
    trial_date = fields.Date(string='Trial Date', track_visibility='onchange')
    notify_trial_date = fields.Date(string='Notify Date')
    notify_trial_date_week = fields.Date(string='Notify Date Week')
    # Count
    tasks_count = fields.Float(string="Tasks", compute="_compute_counts")
    expense_count = fields.Float(
        string='Expense Count', compute='_compute_counts')
    claims_count = fields.Integer(
        string='Claims Count', compute='_compute_claim_counts')
    trails_count = fields.Float(string='Trails', compute='_compute_counts')
    charges_count = fields.Float(string='Charges', compute='_compute_counts')
    court_fees_count = fields.Float(
        string='Charges', compute='_compute_counts')
    case_task_ids = fields.One2many(
        'project.task', 'case_id', string='Task')
    penalties_count = fields.Float(
        string='Penalties', compute='_compute_case_penalties_counts')
    
    observations_count = fields.Float(
        string='Discipline', compute='_compute_counts')
    # NoteBook Record
    claim_ids = fields.One2many("matter.claim", "case_id", string="Claims")
    claim_transation_ids = fields.One2many('claim.distribution.transaction','case_id',string="claim transction")
    payment_schedule_ids = fields.One2many('payment.schedule','case_id',string="Payment Schedule") 
    expense_ids = fields.One2many("hr.expense", "case_expense_id", string="Expense")
    case_do_ids = fields.One2many(
        'case.discipline', 'case_do_id', string='Discipline')
    case_charges_ids = fields.One2many(
        'case.charge', 'case_name', string='Case Charges')
    case_trail_ids = fields.One2many(
        'case.trail', 'matter_name', string='Trail')
    case_judgement_ids = fields.One2many('case.trail.judgement','case',string="judgement")
    case_penalties_ids = fields.One2many(
        'penalties.form', 'matter_id', string='Penalties')
    court_fees_ids = fields.One2many(
        'court.fees', 'matter_id', string='Court Fees')
    case_documents_ids = fields.One2many(
        'matter.document', 'matter_document_id', string='Documents')
    m_doc_count = fields.Integer(
        compute="_compute_mdoc_count", string='Document')
    case_result = fields.Selection([('cases_on_going','On Going'),('won','Won'),
        ('lost','Lost'),('settlement','Settlement')])
    case_judgement_ids = fields.One2many('case.trail.judgement','case',string="judgement")
    claim_transation_ids = fields.One2many('claim.distribution.transaction','case_id',string="transaction")
    payment_schedule_ids = fields.One2many('payment.schedule','case_id',string="payment")

    file_number = fields.Char(string="File ID", track_visibility='onchange')
    file_owner = fields.Selection([('lawyer', 'Lawyer'), ('opposition', 'Claimant/Plaintiff Lawyer'), ('client', 'Client'), ('accuse', 'Claimant / Plaintiff'), ('judge', 'Judge'), ('witness', 'Witness')], string="Current File Owner",track_visibility='onchange')
    file_lawyer = fields.Many2one('lawyer.details', string='Lawyer / Officer Dealing',track_visibility='onchange')
    file_opposition_lawyer = fields.Many2one('opposition.lawyer', string='Claimant/Plaintiff Lawyer',track_visibility='onchange')
    file_client = fields.Many2one('client.client', string='Client', track_visibility='onchange')
    file_accuse = fields.Many2one('accuse.details', string='Claimant / Plaintiff', track_visibility='onchange')
    file_judge = fields.Many2one('judge.details', string='Judge', track_visibility='onchange')
    file_witness = fields.Many2one('witness.details', string='Witness', track_visibility='onchange')
    
    _sql_constraints = [
    ('name_uniq', 'UNIQUE(caseid)', 'Cause ID Must Be Unique!'),
    ('file_number_uniq', 'UNIQUE(file_number)', 'File Number Must Be Unique!'),
    ]

    @api.model
    def create(self, values):
        if values.get('matter_seq', 'New Matter') == 'New Matter':
            values['matter_seq'] = self.env['ir.sequence'].next_by_code(
                'matter.matter') or 'New Matter'
        res = super(MatterMatter, self).create(values)
        project_data = self.env['project.project'].create({
            'name': res.matter_seq, 'case_id': res.id})
        res.project_id = project_data.id
        return res

    # @api.onchange('court_category')
    # def count_court_category(self):
    #     if self.court_category:
    #         return {'domain': {'court_id': [('court_category', '=', self.court_category.id)]}}

    # Count
    @api.multi
    def _compute_counts(self):

        for rec in self:
            task_data = self.env['project.task'].search(
                [('case_id', '=', self.id)])
            if task_data:
                rec.tasks_count = len(task_data)

            expense_data = self.env['hr.expense'].search(
                [('case_expense_id', '=', self.id)])
            if expense_data:
                rec.expense_count = len(expense_data)

            trail_data = self.env['case.trail'].search(
                [('matter_name', '=', self.id)])
            if trail_data:
                rec.trails_count = len(trail_data)

            charges_data = self.env['case.charge'].search(
                [('case_name', '=', self.id)])
            if charges_data:
                rec.charges_count = len(charges_data)

            court_data = self.env['court.fees'].search(
                [('matter_id', '=', self.id)])
            if court_data:
                rec.court_fees_count = len(court_data)
                
            observations_data = self.env['case.discipline'].search(
                [('case_do_id', '=', self.id)])
            if observations_data:
                rec.observations_count = len(observations_data)
            penalties_data = self.env['penalties.form'].search(
                [('matter_id', '=', self.id)])
            if penalties_data:
                rec.penalties_count = len(penalties_data)


    @api.multi
    def _compute_case_penalties_counts(self):
        PenaltiesLine = self.env['penalties.form']
        for penalties in self:
            penalties.penalties_count = PenaltiesLine.search_count(
                [('matter_id', '=', penalties.id)])


    @api.multi
    def _compute_claim_counts(self):
        claimLine = self.env['matter.claim']
        for claim in self:
            claim.claims_count = claimLine.search_count(
                [('case_id', '=', claim.id)])

    # Button
    @api.multi
    def task_action(self):
        self.ensure_one()
        action_rec = self.env.ref('project.action_view_task')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_id', 'in', [self.id])]
            action['context'] = (
                {'default_case_id': self.id, 'default_project_id': self.project_id.id})
            return action

    @api.multi
    def expense_action(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'hr_expense.hr_expense_actions_my_unsubmitted')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_expense_id','=',self.id)]
            action['context'] = ({ 
                                  'default_case_expense_id': self.id})
            return action

    @api.multi
    def claim_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.matter_claim_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_id', '=',self.id)]
            action['context'] = ({'default_case_id': self.id,
                                'default_court_id':self.court_id.id,
                                })
            return action

    @api.multi
    def case_trails_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.case_trail_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('matter_name', '=', self.id)]
            action['context'] = ({'default_matter_name': self.id,
                                  'default_client_name': self.client_name.id,
                                  'default_accuse_name':self.accused.id,
                                  'default_lawyer_name': self.assign_id.id,
                                  'default_opposition_lawyer_name':self.opp_lawyer_id.id,
                                  'default_judge_name':self.judge_id.id,
                                  'default_court_name':self.court_id.id,
                                  })
            return action

    @api.multi
    def case_charges_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.action_case_charge')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_name', '=', self.id)]
            action['context'] = ({'default_case_name': self.id,
                                  'default_client_name': self.client_name.id,
                                  })
            return action

    @api.multi
    def case_penalties_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.window_penalties_form')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('matter_id', '=', self.id)]
            action['context'] = ({'default_matter_id': self.id,
                                  'default_case_id': self.id,
                                  'hide_matter_id_field': True,
                                  'default_client_name_id': self.client_name.id,
                                  'default_accuse_name_id': self.accused.id,
                                  })
            return action

    @api.multi
    def court_fee_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.court_fees_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('matter_id', '=', self.id)]
            action['context'] = ({'default_matter_id': self.id,
                                  'default_client_name': self.client_name.id,
                                  'default_accuse_name': self.accused.id,
                                  'default_court_name':self.court_id.id,
                                  })
            return action

    @api.multi
    def observations_count_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.discipline_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_do_id', '=', self.id)]
            action['context'] = ({'default_case_do_id': self.id,
                                  })
            return action

    @api.multi
    def case_document_action(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.case_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('case_do_id', '=', self.id)]
            action['context'] = ({'default_case_do_id': self.id,
                                  })
            return action

    @api.multi
    def _compute_mdoc_count(self):
        matDocLine = self.env['matter.document']
        for doc in self:
            doc.m_doc_count = matDocLine.search_count(
                [('matter_document_id', '=', doc.id)])

    @api.multi
    def case_documents_action(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.matter_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('matter_document_id', 'in', [self.id])]
            action['context'] = ({'default_matter_document_id': self.id})
            return action

    @api.multi
    def get_document_sequence_vals(self):
        return {
            'name': '%s' % (self.matter_seq),
            'padding': 4,
            'prefix': self.name,
            'code': '%s' % (str(self.id)),
            'number_increment': 1,
        }

    @api.onchange('trial_date')
    def onchange_trial_date(self):
        if self.trial_date:
            self.notify_trial_date = datetime.strptime(
                self.trial_date, '%Y-%m-%d') - relativedelta(days=1)
            self.notify_trial_date_week = datetime.strptime(
                self.trial_date, '%Y-%m-%d') - relativedelta(days=7)

    @api.multi
    def get_client_ids(self):
        mail_ids = ','.join([c.client_emailP for c in self.client_name_many])
        return mail_ids

    @api.multi
    def get_accuse_ids(self):
        mail_ids = ','.join([a.accuse_email for a in self.accuse_ids])
        return mail_ids

    # Client trial update on week befor and day befor trial
    @api.model
    def _send_trail_secheduler_email_client(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'email_template_trail_notification_client')[1]
        record = temp_obj.browse(trail_template_id)
        today = datetime.now()
        context = {}
        today_month_day = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
        trail_ids = self.search([('notify_trial_date', 'like', today_month_day)])
        trail_ids_week = self.search([('notify_trial_date_week', 'like', today_month_day)])
        for trail_id in trail_ids:
            if trail_id.client_name_many:
                record.send_mail(trail_id.id, force_send=True)
        for trail_id in trail_ids_week:
            if trail_id.client_name_many:
                record.send_mail(trail_id.id, force_send=True)

    # Lawyer trial update on week befor and day befor trial
    @api.model
    def _send_trail_secheduler_email_lawyer(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'email_template_trail_notification_lawyer')[1]
        record = temp_obj.browse(trail_template_id)
        today = datetime.now()
        today_month_day = '%-' + \
            today.strftime('%m') + '-' + today.strftime('%d')
        trail_ids = self.search([('notify_trial_date', 'like', today_month_day)])
        trail_ids_week = self.search([('notify_trial_date_week', 'like', today_month_day)])
        for trail_id in trail_ids:
            if trail_id.assign_id.lawyer_emailW:
                record.send_mail(trail_id.id, force_send=True)
        for trail_id in trail_ids_week:
            if trail_id.assign_id.lawyer_emailW:
                record.send_mail(trail_id.id, force_send=True)

    # Judge trial update on week befor and day befor trial
    @api.model
    def _send_trail_secheduler_email_judge(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'email_template_trail_notification_judge')[1]
        record = temp_obj.browse(trail_template_id)
        today = datetime.now()
        today_month_day = '%-' + \
            today.strftime('%m') + '-' + today.strftime('%d')
        trail_ids = self.search(
            [('notify_trial_date', 'like', today_month_day)])
        for trail_id in trail_ids:
            if trail_id.judge_id.judge_emailW:
                record.send_mail(trail_id.id, force_send=True)

    # Opposition Lawyer trial update on week befor and day befor trial
    @api.model
    def _send_trail_secheduler_email_opp_lawyer(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'email_template_trail_notification_opp_lawyer')[1]
        record = temp_obj.browse(trail_template_id)
        today = datetime.now()
        today_month_day = '%-' + \
            today.strftime('%m') + '-' + today.strftime('%d')
        trail_ids = self.search(
            [('notify_trial_date', 'like', today_month_day)])
        for trail_id in trail_ids:
            if trail_id.opp_lawyer_id.opposition_emailW:
                record.send_mail(trail_id.id, force_send=True)

    # Accuse trial update on week befor and day befor trial
    @api.model
    def _send_trail_secheduler_email_accuse(self):
        temp_obj = self.env['mail.template']
        trail_template_id = self.env['ir.model.data'].get_object_reference(
            'law_management', 'email_template_trail_notification_accuse')[1]
        record = temp_obj.browse(trail_template_id)
        today = datetime.now()
        today_month_day = '%-' + \
            today.strftime('%m') + '-' + today.strftime('%d')
        trail_ids = self.search(
            [('notify_trial_date', 'like', today_month_day)])
        for trail_id in trail_ids:
            # if trail_id.accused.accuse_email:
            if trail_id.accuse_ids:
                record.send_mail(trail_id.id, force_send=True)


class MatterName(models.Model):
    _name = 'matter.name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=False,
                       track_visibility='onchange')


class MatterCategory(models.Model):
    _name = 'matter.category'
    _order = 'create_date desc'
    _rec_name = 'code'

    matter_name = fields.Many2one('matter.name', string='Name')
    code = fields.Char(string='Code', track_visibility='onchange')
    type = fields.Selection(
        [('civil', 'Civil')],default='civil', string='Type', track_visibility='onchange')


class MatterDocument(models.Model):
    _name = 'matter.doc'
    _rec_name = 'attach_id'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    doc_name = fields.Char(string='Name', track_visibility='onchange')
    doc_desc = fields.Text(string='Description', track_visibility='onchange')
    attach_id = fields.Many2many('ir.attachment', string='Attachments')
    case_doc_id = fields.Many2one('matter.matter', string='Case Document')


class CaseHistory(models.Model):
    _name = 'case.history'
    _order = 'create_date desc'
    _rec_name = 'date'
    _inherit = ['mail.thread']

    date = fields.Date(string='Date', track_visibility='onchange')
    user = fields.Many2one('res.users', string="Created By",
                           default=lambda self: self.env.user, readonly="True")
    stage_id = fields.Many2one(
        'case.stages', string='Stage', track_visibility='onchange')
    case_history_id = fields.Many2one('matter.matter', string='History')


class MatterDocuments(models.Model):
    _name = 'matter.document'
    _order = 'create_date desc'
    _rec_name = 'matter_document_id'

    mat_doc_name = fields.Char(string='Document Name', track_visibility='onchange')
    document_case_name = fields.Char(related='matter_document_id.case_name', string='Case Name')
    doc_no = fields.Char(string='Document No.')
    mat_doc_id = fields.Many2many('ir.attachment',string='Attachments')
    mat_comment = fields.Text(string='Description')
    mat_date = fields.Date(string='Date')
    mat_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    matter_document_id = fields.Many2one('matter.matter',string="Case Number")
    category_id = fields.Many2one('document.category')
    category_type = fields.Selection([('Plaintiff Lawyer Document','Plaintiff Lawyer Document'),('Lawyer Document','Lawyer Document')],string='Category Type')