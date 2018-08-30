from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
class BaRoomType(models.Model):
    _name = 'ba.room.type'
    _descrition = 'Room Type'
    name = fields.Char('Name',require=True)
    image_medium = fields.Binary(
        "Medium-sized image")
    image = fields.Binary(
        "Big-sized image")
    internal_notes = fields.Text('Internal Notes')
    company = fields.Many2one('res.company',string='Company')
    active = fields.Boolean('Active?',default=True)
    base_occ = fields.Integer('Base Occupancy',required=True)
    max_occ = fields.Integer('Max Occupancy', required=True)
    rack_rate = fields.Float('Rack Rate',required=True)
    cost = fields.Float('Cost', required=True)
    facilities = fields.Many2many('ba.facilities',string='Facilities')
    amenities = fields.Many2many('ba.amenities',string='Amenities')
    rate_type = fields.Many2many('ba.rate.type',string='Rate Type')
    package = fields.Many2many('ba.packages',string="Package")
    internal_notes = fields.Text('Internal Notes')
    @api.model
    def create(self,values):
        record = super(BaRoomType, self).create(values)
        product = self.env['product.product'].create({
            'name':values['name'],
            'type':'product',
            'categ_id':1,
            'sale_ok':'true',
            'tracking':'serial',
            'standard_price':values['cost'],
            'list_price':values['rack_rate']

            })
        return record