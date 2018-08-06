from odoo import fields, models, api
import datetime

class ProductRoom(models.Model):
	_name = 'ba.product.room'

	date = fields.Date('Date',default=datetime.datetime.now())
	room = fields.Many2one('ba.rooms','Room')
	room_type = fields.Many2one('ba.room.type','Room Type')
	lots = fields.Many2one('stock.production.lot','Serial No')
	availability = fields.Boolean('Availability')


