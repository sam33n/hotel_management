from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError



class BaNightAudit(models.Model):
    _name = 'ba.night.audit'
    _description = 'Night Audit'
    code = fields.Char('Code',required=True)
    audit_date = fields.Date('Audit Date',required=True,default=fields.Date.today())
    ip_address = fields.Char('IP Address',required=True)
    entries_posted = fields.Char('Entries Posted',required=True)
    entries_issue = fields.Char('Entries with Issues',required=True)
    room_nights_perished = fields.Char('Perished Room')
    room_nights_created = fields.Char('Room Nights Created')