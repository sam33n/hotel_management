from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaFacilities(models.Model):
    _name= 'ba.facilities'
    _description = 'Facilities'
    image_medium = fields.Binary(
        "Medium-sized image")
    name = fields.Char('Facility',required=True)
    code = fields.Char('Code', required=True)
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    status = fields.Boolean('Active?',default=True)