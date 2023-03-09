# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseReportOut(models.Model):
    _name = 'reference.evidence'
    _rec_name='name'

    name = fields.Char('Name', default="Evidence")

    @api.multi
    def transfer_salected_evidence(self):
        active_id = self._context['active_ids']
        evidence_obj = self.env['case.trail.reference.evidence']
        if active_id:
            case_evidences = []
            matters = []
            trials = []
            judgement_list = []
            for evidence_id in active_id:
                trial_evidence = self.env['case.trail.evidance'].browse(evidence_id)
                judgement_list.append(trial_evidence.judgment_id)
                matters.append(trial_evidence.evidance_case)
                trials.append(trial_evidence.trail_evidance_id)
                case_evidences.append(trial_evidence)
    
            case_a = [matter.id for matter in matters]
            trial_a = [trial.id for trial in trials]
            # judgement = self.env['case.trail.judgement'].search([('trail_judgement_id','in',trial_a)])
            for imp_evidence in case_evidences:
                evidence_line = evidence_obj.create({
                    'trail_name':imp_evidence.evidance_case.id,
                    'reference_evidence':imp_evidence.evidance_name.id,
                    'case':imp_evidence.evidance_case.matter_seq,
                    'lawyer':imp_evidence.evidance_lawyer.id,
                    'opposition_lawyer':imp_evidence.evidance_opposition_lawyer.id,
                    })
                judgement_list[0].write({'reference_evidence_ids': [(4, evidence_line.id)]})
        else:
            raise UserError(_('No evidence selected, please select the evidence.'))
        return {
            'name': _('Judgement'),
            'view_mode': 'form',
            'view_id': self.env.ref('law_management.view_case_trail_judgement_form').id,
            'src_model': 'reference.evidence',
            'res_model': 'case.trail.judgement',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': judgement_list[0].id or False
        }

    @api.multi
    def cancel_salected_evidence(self):
        return {
            'name': _('Judgement'),
            'view_mode': 'tree',
            'view_id': self.env.ref('law_management.view_case_trail_judgement_tree').id,
            'src_model': 'reference.evidence',
            'res_model': 'case.trail.judgement',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
