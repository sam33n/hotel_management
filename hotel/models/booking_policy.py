from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaBookingPolicy(models.Model):
    _name = 'ba.booking.policies'
    _description = 'Booking Policy'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    days_before_arrival = fields.Integer('Days Before Arrival',required=True)
    chagre = fields.Float('Cancellation Charge',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    status = fields.Boolean('Active?',required=True)
    package = fields.Many2many('ba.packages',string='Packages')
    rate_type = fields.Many2many('ba.rate.type',required=True)