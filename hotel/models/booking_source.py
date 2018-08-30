from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError



class BaBookingSource(models.Model):
    _name = 'ba.booking.source' 
    _description = 'Booking Source'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    valid_from = fields.Date('Valid From',required=True,default = fields.Date.today())
    valid_to = fields.Date('Valid To',required=True,default = fields.Date.today())
    booking_policies  = fields.Many2one('ba.booking.policies',string='Booking Policies')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policies')
    booking_type = fields.Selection([('direct_booking','Direct Booking'),('ota','OTA'),('walkin','Walkin'),('corporate_travel_agent','Corporate Travel Agent')])
    rate_type = fields.Many2one('ba.rate.type',string='Rate Type')
    package = fields.Many2many('ba.packages',string='Package')
    booking_source_category = fields.Many2one('ba.booking.source.category',string='Booking Source Category')
    @api.onchange('booking_source_category')
    def onchage_booking_source_category(self):
    	self.booking_policies = self.booking_source_category.booking_policies
    	self.cancellation_policies = self.booking_source_category.cancellation_policies
    	self.rate_type = self.booking_source_category.rate_type
    	self.package = self.booking_source_category.package