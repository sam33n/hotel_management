from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaReservationLine(models.Model):
    _name = 'ba.reservation.line'
    _description ='Reservation line'
    reservation_id = fields.Many2one('ba.reservation','Reservation Reference', ondelete='cascade')
    room_type_line = fields.Many2one('ba.room.type','Room Type')
    room_cost = fields.Float('Price')
    quantity = fields.Integer('Quantity', default=1)
    customer = fields.Many2one('res.partner',string='Customer')
    package = fields.Many2one('ba.packages',string='Package')
    arrival_date = fields.Date('Arrival Date',required=True,default= fields.Date.today())
    departure_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    booking_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    @api.onchange('booking_date')
    def set_customers(self):
        print(self.reservation_id.customer)
        if self.reservation_id.customer:
            self.customer = self.reservation_id.customer
        else:
            pass
        if self.reservation_id.arrival_date:
            self.arrival_date = self.reservation_id.arrival_date
        else:
            pass
        if self.reservation_id.departure_date:
            self.departure_date = self.reservation_id.departure_date
        else:
            pass
            