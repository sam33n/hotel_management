from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaStay(models.Model):
    _name = 'ba.stay'
    _description = 'Stay'
    code = fields.Char('Code',required=True)
    res = fields.Char('Res_ID',required=True)
    adults = fields.Integer('Adults',required=True)
    children = fields.Integer('Children',required=True)
    infants = fields.Integer('Infants',required=True)
    arrival_date = fields.Date('Arrival Date',required=True,default= fields.Date.today())
    departure_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    other_consumption = fields.Char('Other_Consumption',required=True)
    stay_status = fields.Selection([('not_started','Not Started'),('in_house','In-House'),('checked_out','Checked-Out')])
    rooms = fields.Many2one('ba.rooms',string='Rooms')
    amount = fields.Float('Amount')
    additional_bill_transfer = fields.Char('Additional Bill Transfer')

    package = fields.Many2many('ba.packages',string='Package')
    apply_inclusion = fields.Many2many('ba.amenities',string='Apply Inclusion')
    wastage_broken_stuff_amount = fields.Integer('Wastage/Broken Stuff Amount')
