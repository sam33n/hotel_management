from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError



class BaSection(models.Model):
    _name = 'ba.section'
    _description = 'Section'
    name= fields.Char('Name',required=True)
    code = fields.Char('Code', required=True)
    rooms= fields.Many2many('ba.rooms',string='Rooms')
    company=fields.Many2one('res.company',required=True,string='Company')
    active = fields.Boolean('Active?',default=True)