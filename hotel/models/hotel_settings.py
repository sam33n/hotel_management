from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaHotelSettings(models.TransientModel):
    _name = 'ba.hotel.settings'
    _inherit = 'res.config.settings'
    _description = 'Hotel Settings'
    checkin_time = fields.Float('Checkin Time',required=True)
    checkout_time = fields.Float('Checkout Time',required=True)
    child_age = fields.Integer('Child Age',required=True)
    infant_age = fields.Integer('Infant Age',required=True)
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')
    different_rate_for_weekend = fields.Boolean('Different Weekend Rate')
    @api.model
    def get_default_values(self,fields):
	conf = self.env['ir.config_parameter']
	checkin = float(conf.get_param('checkin_time'))
	check_out = float(conf.get_param('checkout_time'))
	monday = (conf.get_param('monday'))
	print(check_out,type(monday))
	#check_out  = check_out.split(',')
	
	#for c in check_out:
	#    checkout =c[1:-2]
	return {
	     
            'checkin_time': float(conf.get_param('checkin')),
	    'checkout_time':float(conf.get_param('checkout')),
	    'child_age':int(conf.get_param('child_age')),
	    'infant_age':int(conf.get_param('infant_age')),
	    'monday':(conf.get_param('monday')),
	    'tuesday':(conf.get_param('tuesday')),
	    'wednesday':(conf.get_param('wednesday')),
	    'thursday':(conf.get_param('thursday')),
	    'friday':(conf.get_param('friday')),
	    'saturday':(conf.get_param('saturday')),
	    'sunday':(conf.get_param('sunday')),
	    'different_rate_for_weekend':(conf.get_param('different_rate_for_weekend')),
        }
	"""return{
		'checkin_time':self.checkin_time,
		'checkout_time':self.checkout_time
		
	}"""
    @api.one
    def set_default_values(self):
        conf = self.env['ir.config_parameter']
        conf.set_param('checkin_time', self.checkin_time)
        conf.set_param('checkout_time', self.checkout_time)
        conf.set_param('child_age', self.child_age)
        conf.set_param('infant_age', self.infant_age)
        conf.set_param('monday', self.monday)
        conf.set_param('tuesday', self.tuesday)
        conf.set_param('wednesday', self.wednesday)
        conf.set_param('thursday', self.thursday)
        conf.set_param('friday', self.friday)
        conf.set_param('saturday', self.saturday)
        conf.set_param('sunday', self.sunday)
        conf.set_param('different_rate_for_weekend', self.different_rate_for_weekend)

	#checkin_time  = self.checkin_time
	#checkout_time = self.checkout_time