from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError

class BaRateType(models.Model):
    _name = 'ba.rate.type'
    _description = 'Rate Type'
    name = fields.Char('Rate Name',required=True)
    code = fields.Char('Code',required= False)
    image_medium = fields.Binary(
        "Medium-sized image")
    company = fields.Many2one('res.company',string='Company')
    valid_from = fields.Date('Valid From',required=True,default=fields.Date.today())
    valid_till = fields.Date('Valid Till',required=True,default =fields.Date.today())
    active = fields.Boolean('Active?',default=True)
    seasons = fields.Selection([('peak','Peak'),('high','High'),('medium','Medium'),('low','Low')])
    room_type = fields.Many2many('ba.room.type',string='Room Type')
    source = fields.Many2many('ba.booking.source',string='Booking Source')
    amenities = fields.Many2many('ba.amenities',string='Amenities')
    amount_per_night = fields.Float('Amount Per Night')
    additional_person_charge = fields.Float('Additional Person Charge')
    additional_child_charge = fields.Float('Additional Child Charge')
    additional_infant_charge = fields.Float('Additional Infant Charge')