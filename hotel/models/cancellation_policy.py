from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError



class BaCancellationPolicy(models.Model):
    _name = 'ba.cancellation.policies'
    _description = 'Cancellation Policy'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    days_before_arrival = fields.Integer('Days Before Arrival',required=True)
    cancellation_charges_in = fields.Selection([('fixed_amounnt','Fixed Amount'),('percentage','Percentage'),('room_night','Room Night')])
    chagre = fields.Float('Cancellation Charge',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    status = fields.Boolean('Active?',required=True)