from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class BaReservation(models.Model):
    _name = 'ba.reservation'
    _description = 'Reservation'
    code = fields.Char('Code',default=True)
    customer = fields.Many2one('res.partner',string='Customer',required=True)
    adults = fields.Integer('Adults',required=True)
    children = fields.Integer('Children',required=True)
    infants = fields.Integer('Infants',required=True)
    room_cost = fields.Float('Price')
    amenities = fields.Many2many('ba.amenities',string='Amenities')
    booking_date = fields.Date('Booking Date',required=True,default= fields.Date.today())
    arrival_date = fields.Date('Arrival Date',required=True,default= fields.Date.today())
    departure_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    group_booking = fields.Many2one('ba.group.booking',string='Group Booking')
    booking_source = fields.Many2one('ba.booking.source',string='Booking Source')   
    rate_type = fields.Many2one('ba.rate.type',string='Rate Type')
    other_consumption = fields.Char('Other Consumption')
    paid_status = fields.Boolean('Paid' , compute='_onchange_paid_status')
    reservation_status = fields.Selection([('tentative','Tentative'),('confirmed','Confirmed'),('no_show','  No Show'),('checked_in','Checked In')])
    amount = fields.Float('Amount')
    booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
    reservation_line = fields.One2many('ba.reservation.line','reservation_id',string='Reservation Line')
    



    @api.model
    def create(self,values):
        rec = super(BaReservation, self).create(values)
        print(rec)
        print(rec.id)
        sale_order = self.env['sale.order'].create({
            'date_order':values['booking_date'],
            'partner_id':values['customer'],
            'amount_total':values['amount'],
            'reservation_id':rec.id
            

            })
        print(sale_order)
        for line in rec.reservation_line:
            print(line.room_type_line)
            print(line.room_type_line.amenities)

            room_type_name = self.env['product.product'].search([('name','=',line.room_type_line.name )])
            line.room_cost = room_type_name.list_price
            print(line.room_cost)

            print(room_type_name)
            amenities_total = 0

            for lines in line.room_type_line.amenities:
                print(lines.amount)
                amenities_total += lines.amount

            prices = room_type_name.list_price + amenities_total
            product_quantity = line.quantity
            print(product_quantity)
            product_unit = room_type_name.uom_id.id
            sale_order_line = self.env['sale.order.line'].create({
                    'order_id':sale_order.id,
                    'product_id':room_type_name.id,
                    'price_unit':prices,
                    'product_uom_qty':product_quantity,
                    'product_uom':product_unit

                })
            print(sale_order_line)
        return rec

    
    
    
    @api.onchange('paid_status')
    def _onchange_paid_status(self):
        #obj = self.env['account.invoice'].search([])
        obj = self.env['sale.order'].search([])
        print(obj)
        for line in obj:
            data = line.filtered(lambda r: r.invoice_ids.state == "paid" )
            print(data)
        #print(line.reservation_id.paid_status)

        #line.reservation_id.paid_status = ( True if line.invoice_ids.state =='paid' else False )
        #print(line.reservation_id.paid_status)
        #print(line.state == 'paid')
        #print( 'ifelse',True if line.state == 'paid' else False)
        #status = ( True if line.state == 'paid' else False)
        #print(status)


    @api.multi
    def action_sale_order_info(self):
        view_id = self.env.ref('sale.view_order_form').id
        print(view_id)
        return {
            'name':'view_order_form',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'sale.order',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':self.id,
            'target':'new',
        }



                




        
            



            

        

            



                

            
        