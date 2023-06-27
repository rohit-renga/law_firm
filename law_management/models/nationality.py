# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class Nationality(models.Model):
    _name = 'nationality.master'
    _description = 'Nationality'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name' , required=False)
    nationality_code = fields.Char(string='ID')
    ph_street = fields.Char(string='Street', track_visibility='onchange')
    ph_street2 = fields.Char(
        string='Street2..', track_visibility='onchange')
    ph_city_id = fields.Char(
        string='City', track_visibility='onchange')
    ph_district_id = fields.Char(string='District', track_visibility='onchange')

    ph_village = fields.Char(string='Village', track_visibility='onchange')
    ph_state_id = fields.Many2one('res.country.state',
                               string='State', track_visibility='onchange')
    ph_zip = fields.Char(string='zip',
                      track_visibility='onchange')
    ph_country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')
    po_street = fields.Char(string='Street', track_visibility='onchange')
    po_street2 = fields.Char(
        string='Street2..', track_visibility='onchange')
    po_city_id = fields.Char(
        string='City', track_visibility='onchange')
    po_district_id = fields.Char(string='District', track_visibility='onchange')

    po_village = fields.Char(string='Village', track_visibility='onchange')
    po_state_id = fields.Many2one('res.country.state',
                               string='State', track_visibility='onchange')
    po_zip = fields.Char(string='zip',
                      track_visibility='onchange')
    po_country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')

    _sql_constraints = [('name_unique', 'unique(name)',
                     'Nationality Name Must Be Unique!!!')]