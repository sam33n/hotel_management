from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaRooms(models.Model):
    _name ='ba.rooms'
    _description = 'Rooms'
    name= fields.Char('Name',required=True)
    code = fields.Char('Code', required=True)
    active = fields.Boolean('Active?',default=True)
    room_type = fields.Many2one('ba.room.type',string='Room Type',required=True)
    room_status = fields.Selection([('free','Free'),('occupied','Occupied'),('would_free','Would be Free'),('would_accupied','Would be Occupied'),('under_maintenance','Under Maintenance'),('blocked','Blocked')])
    housekeeping_status = fields.Selection([('clean','Clean'),('dirty','Dirty')])
    floor = fields.Many2one('ba.floor',string='Floor')
    section = fields.Many2one('ba.section',string='Section')
    starting_date = fields.Date('Start Date', required=True, default=fields.Date.today())
    smoking = fields.Boolean('Smoking')
    pets_allowed = fields.Boolean('Pets Allowed?')
    """@api.multi
    def date_get(self):
	date =self.starting_date
	print(date)
	return date
    """
    @api.model
    def run(self,use_new_cursor=False, company_id=False):
        print('hello')
        now = datetime.datetime.now()
        rooms  = self.env['ba.rooms'].search([])
        print(rooms)

        room_list = []
        for line in rooms:
            product = self.env['product.product'].search([('name','=', line.room_type.name)])
            room_list.append(product)
        print(room_list)


        for room in rooms:
            print('hii')
            product = self.env['product.product'].search([('name','=',room.room_type.name)])
            #product = self.env['product.product'].browse([room.id])
            print(product)
            print(room.code)
            print(product.id)

            
            try:
                print('in try')
                print(str(now.strftime("%Y-%m-%d")))
                all_lots = self.env['stock.production.lot'].search([])
                print(all_lots)
                print([i.name for i in all_lots])
                new_code =(room.code +'/' +str(now.strftime("%Y-%m-%d")))
                if new_code in [i.name for i in all_lots]:
                    pass
                #if (room.code +'/' +str(now.strftime("%Y-%m-%d")) in 
                else:
                    lot = self.env['stock.production.lot'].create({
                        'name':room.code +'/' +str(now.strftime("%Y-%m-%d")),
                        'product_id':product.id,
                        })
                    print('lot')

                    stock_inv = self.env['stock.inventory'].create({
                        'name':'INV:' +lot.name,
                        'filter':'product',
                        'product_id':product.id,
                        'location_id':15,
                        'date':str(now.strftime("%Y-%m-%d")),
                        'state':'done'
                        })
                    print('stock_inv')

                    stock_inv_line = self.env['stock.inventory.line'].create({
                        'theoretical_qty':1,
                        'product_qty':1,
                        'location_id':15,
                        'company_id':1,
                        'inventory_id':stock_inv.id,
                        'product_id':product.id,
                        'inventory_location_id':15,
                        'prod_lot_id':lot.id,
                        'state':'done'
                        })
                    print('stock_inv_line')

                    stock_quant = self.env['stock.quant'].create({
                        'product_id':product.id,
                        'qty':1,
                        'lot_id':lot.id,
                        'location_id':15,

                        })
                    print('stock_quant')
                    stock_move = self.env['stock.move'].create({
                        'name':'INV:' +lot.name,
                        'product_id':product.id,
                        'product_uom_qty':1,
                        'product_uom':1,
                        #'priority':1,
                        #'quant_ids':stock_quant.id,
                        'location_id':15,
                        'location_dest_id':15,

                        })
                    print('stock_move')
                

            except Exception as e:
                print('in except',e)
                pass