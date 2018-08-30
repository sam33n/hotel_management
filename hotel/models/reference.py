from odoo import models, fields, api, _


class ReferenceModel(models.Model):
	_inherit = 'sale.order'
	_description = 'Reference'

	reservation_id = fields.Many2one('ba.reservation', string='Reservation ID')

            
	        
