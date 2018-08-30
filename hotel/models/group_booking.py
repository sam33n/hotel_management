from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaGroupBooking(models.Model):
    _name = 'ba.group.booking'
    _description = 'Group Booking'
    name = fields.Char('Name',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    rate_type = fields.Many2many('ba.rate.type',string='Rate Type')
    customer = fields.Many2many('res.partner',string='Customer')
    package = fields.Many2many('ba.packages',string='Packages')
    booking_source = fields.Many2one('ba.booking.source',required=True)
    adults = fields.Integer('Adults',required=True)
    children = fields.Integer('Children',required=True)
    infants = fields.Integer('Infants',required=True)