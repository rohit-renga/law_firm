
{
    'name': 'Law Management ERP',
    'version': '1.0',
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'category': 'Sales',
    'author': ['Indimedi Sol. Pvt Ltd'],
    'summary': '',
    'description' : """ Base Module of Law Management ERP
    
""",
    'depends': ['base', 'sale', 'hr_expense', 'account', 'hr','board' ,'web','mail','project_task_default_stage'],
    'data': [

            'data/sequence.xml',
            'data/doc.xml',
            'data/trail_scheduler_lawyers.xml',
            'data/trail_scheduler_clients.xml',
            'data/trail_scheduler_accuses.xml',
            'data/trail_scheduler_opposition_lawyers.xml',
            'data/trail_scheduler_judges.xml',
            'data/task_scheduler_for_lawyers.xml',
            'data/trail_email_notification_lawyers.xml',
            'data/trail_email_notification_clients.xml',
            'data/lawyer_task_notification_email_templates.xml',
            'security/law_management_security.xml',
            'security/menu_security.xml',
            'security/ir.model.access.csv',
            # 'views/export.xml',
            #'views/button_view.xml',
            'views/res_user_view.xml',
            'views/case_management_view.xml',
            'views/master_data_view.xml',
            'views/configuration_view.xml',
            'views/nationality_view.xml',
            'views/secretary_view.xml',
            'views/registrar_view.xml',
            #'views/res_partner_view.xml',
            'views/client_view.xml',
            'views/lawyer_view.xml',
            'views/opposition_lawyer_view.xml',
            'views/judge_view.xml',
            'views/witness_view.xml',
            'views/plaintiff_view.xml',
            'views/accuse_view.xml',
            'views/court_view.xml',
            'views/court_admin.xml',
            'views/case_clerk.xml',
            'views/case_view.xml',
            'views/account_view.xml',
            'views/law_code_view.xml',
            'views/matter_view.xml',
            'views/case_trail_view.xml',
            'views/evidance_view.xml',
            'views/judgement_view.xml',
            'views/case_charges_view.xml',
            'views/court_fees_view.xml',
            'views/claim_view.xml',
            'views/claim_distribution_view.xml',
            'views/claim_transaction_view.xml', 
            'views/disciplinary_observation_view.xml',
            'views/penalties_view.xml',
            'views/payment_schedule_view.xml',
            'views/hr_expense_view.xml',         
            'views/acts_view.xml',
            'views/articles_view.xml',
            'views/project_view.xml',
            'views/dashboard.xml',
            'wizard/refence_evidence_view.xml',
            'views/defendent_view.xml',


    ],
    'qweb': [
        'static/src/xml/base.xml'],
    'installable': True,
    'application': False,
}
