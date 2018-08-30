from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError

class BaAmenities(models.Model):
    _name = 'ba.amenities'
    _description = 'Amenities'
    image_medium = fields.Binary(
        "Medium-sized image")
    name= fields.Char('Amenity',required=True)
    code = fields.Char('Code',required=True)
    chargeable_or_not = fields.Boolean('Chargeable?',default=True)
    amenities_type = fields.Selection([('per_reservation','Per Reservation'),('per_room','Per Room'),('check-in','Check-in'),('check-out','Check-out'),('nth_day','Nth Day'),('-nth_day','-Nth Day')])
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    amount = fields.Float('Amount')
    status = fields.Boolean('Status?',default=True)
    service_type = fields.Selection([('pick_up','Pick Up'),('drop_off','Drop Off'),('breakfast','Breakfast'),('room_service','Room Service'),('parking_service','Parking Service'),('laundry','Laundry')])

    @api.model
    def create(self,values):
        record = super(BaAmenities, self).create(values)
        print(record)
        product = self.env['product.product'].create({
            'name':values['name'],
            'type':'product',
            'categ_id':1,
            'sale_ok':'true',
            'tracking':'serial',
            'list_price':values['amount']

            })
        return record