from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaBookingSourceCategory(models.Model):
	_name= 'ba.booking.source.category'
	_description='Booking Source Category'
	name=fields.Char('Name',required=True)
	code = fields.Char('Code',required=True)
	booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
	cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
	rate_type = fields.Many2one('ba.rate.type',string='Rate Type')
	package  = fields.Many2many('ba.packages',string='Package')