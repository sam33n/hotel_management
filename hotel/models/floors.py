from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaFloors(models.Model):
    _name = 'ba.floor'
    _description = 'Floor'
    name= fields.Char('Name',required=True)
    code = fields.Char('Code', required=True)
    rooms= fields.Many2many('ba.rooms',string='Rooms')
    level = fields.Integer('Level',required=True)
    company=fields.Many2one('res.company',required=True,string='Company')
    active = fields.Boolean('Active?',default=True)