from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaPackages(models.Model):
    _name = 'ba.packages'
    _description = 'Packages'
    name = fields.Char('Name',required=True)
    code= fields.Char('Code',required=True)
    image_medium = fields.Binary(
        "Medium-sized image")
    internal_notes = fields.Text('Internal Notes')
    terms_condition = fields.Text('Terms and Condition')
    valid_from = fields.Date('Valid From',default=fields.Date.today())
    valid_till = fields.Date('Valid Till',default=fields.Date.today())
    seasons = fields.Selection([('peak','Peak'),('high','High'),('medium','Medium'),('low','Low')])
    minimum_stay = fields.Integer('Minimum Stay',required=True)
    maximum_stay = fields.Integer('Maximum Stay',required=True)
    price = fields.Float('Price',required=True)
    additional_person_charge = fields.Float('Additional Person Charge')
    additional_child_charge = fields.Float('Additional Child Charge')
    additional_infant_charge = fields.Float('Additional Infant Charge')
    default_duration = fields.Date('Date')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
    booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
    booking_source = fields.Many2many('ba.booking.source',string='Booking Source')
    room_type = fields.Many2one('ba.room.type',required=True)
    status = fields.Boolean(string='Status')
    scalable = fields.Char('Scalable')
    extend_stay_type = fields.Selection([('prorata','Prorata'),('double','Double')])
    fixed_start_date = fields.Date('Start Date', required=True, default=fields.Date.today())
    fixed_end_date  = fields.Date('End Date', required=True, default= fields.Date.today())
