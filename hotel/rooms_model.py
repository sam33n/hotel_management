# -*- coding: utf-8 -*-
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


class BaRateType(models.Model):
    _name = 'ba.rate.type'
    _description = 'Rate Type'
    name = fields.Char('Rate Name',required=True)
    code = fields.Char('Code',required= False)
    image_medium = fields.Binary(
        "Medium-sized image")
    company = fields.Many2one('res.company',string='Company')
    valid_from = fields.Date('Valid From',required=True,default=fields.Date.today())
    valid_till = fields.Date('Valid Till',required=True,default =fields.Date.today())
    active = fields.Boolean('Active?',default=True)
    seasons = fields.Selection([('peak','Peak'),('high','High'),('medium','Medium'),('low','Low')])
    room_type = fields.Many2many('ba.room.type',string='Room Type')
    source = fields.Many2many('ba.booking.source',string='Booking Source')
    amenities = fields.Many2many('ba.amenities',string='Amenities')
    amount_per_night = fields.Float('Amount Per Night')
    additional_person_charge = fields.Float('Additional Person Charge')
    additional_child_charge = fields.Float('Additional Child Charge')
    additional_infant_charge = fields.Float('Additional Infant Charge')


class BaAmenities(models.Model):
    _name = 'ba.amenities'
    _description = 'Amenities'
    image_medium = fields.Binary(
        "Medium-sized image")
    name= fields.Char('Amenity',required=True)
    code = fields.Char('Code',required=True)
    chargeable_or_not = fields.Boolean('Chargeable?',default=True)
    amenities_type = fields.Selection([('per_reservation','Per Reservation'),('per_room','Per Room'),('check-in','Check-in'),('check-out','Check-out'),('nth_day','Nth Day'),('-nth_day','-Nth Day')])
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    amount = fields.Float('Amount')
    status = fields.Boolean('Status?',default=True)
    service_type = fields.Selection([('pick_up','Pick Up'),('drop_off','Drop Off'),('breakfast','Breakfast'),('room_service','Room Service'),('parking_service','Parking Service'),('laundry','Laundry')])

    @api.model
    def create(self,values):
        record = super(BaAmenities, self).create(values)
        print(record)
        product = self.env['product.product'].create({
            'name':values['name'],
            'type':'product',
            'categ_id':1,
            'sale_ok':'true',
            'tracking':'serial',
            'list_price':values['amount']

            })
        return record

            


class BaFacilities(models.Model):
    _name= 'ba.facilities'
    _description = 'Facilities'
    image_medium = fields.Binary(
        "Medium-sized image")
    name = fields.Char('Facility',required=True)
    code = fields.Char('Code', required=True)
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    status = fields.Boolean('Active?',default=True)

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
    @api.multi
    def run(self,use_new_cursor=False, company_id=False):
        print('hello')
        now = datetime.datetime.now()
        rooms  = self.env['ba.rooms'].search([])
        print(rooms)
    	
    	for room in rooms:
            print('hii')
            #product = self.env['product.product'].search([('name','=',room.room_type.name)])
            product = self.env['product.product'].browse([room.room_type.id])
            print(product)
            print(room.code)
            print(product.id)

            

            try:
                print('in try')
                print(str(now.strftime("%Y-%m-%d")))
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
                    #'lot_id':lot.id,
                    'location_id':15,

                    })
                print('stock_quant')
                stock_move = self.env['stock.move'].create({
                    'name':'INV:' +lot.name,
                    'product_id':product.id,
                    'product_uom_qty':1,
                    'product_uom':1,
                    'priority':1,
                    'quant_ids':stock_quant.id,

                    })
                print('stock_move')
            

            except Exception as e:
                
                
                print('in except')
                continue
                #lot = self.env['stock.production.lot'].search([('name','=',str(room.code))])
                #print(lot)
                '''stock_update = self.env['stock.change.product.qty'].write({
        			'product_id':product.id,
        			'new_quantity':1,
        			'lot_id':lot.id,
                    'product_tmpl_id': self.env['product.template'].browse([product.id])
        			})
                print(stock_update)
                product_room = self.env['ba.product.room'].create({
                    'room':room.id,
                    'room_type':room.room_type.id,
                    'lots':lot.id
                    })
                print(product_room)'''
''' @api.model
    def create(self,values):
	record = super(BaRooms, self).create(values)
        date =  datetime.datetime.strptime(record.starting_date, '%Y-%m-%d').date()

	date_to_end = date + datetime.timedelta(days=365)
	print(type(date),record.active,record.name,record.code,record.room_status,record.floor)
	if record.floor == []:
	    print('Ho gya kaam')
	print(date_to_end)
	
	while date <= date_to_end:
	
	    print(date)
	    self.env['product.product'].create({
		'name':record.name,
		'type':'service',
		'categ_id':1 })
	    date = date + datetime.timedelta(days=1)
	return record
'''

class BaFloors(models.Model):
    _name = 'ba.floor'
    _description = 'Floor'
    name= fields.Char('Name',required=True)
    code = fields.Char('Code', required=True)
    rooms= fields.Many2many('ba.rooms',string='Rooms')
    level = fields.Integer('Level',required=True)
    company=fields.Many2one('res.company',required=True,string='Company')
    active = fields.Boolean('Active?',default=True)
class BaSection(models.Model):
    _name = 'ba.section'
    _description = 'Section'
    name= fields.Char('Name',required=True)
    code = fields.Char('Code', required=True)
    rooms= fields.Many2many('ba.rooms',string='Rooms')
    company=fields.Many2one('res.company',required=True,string='Company')
    active = fields.Boolean('Active?',default=True)
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
class BaPackages(models.Model):
    _name = 'ba.packages'
    _description = 'Packages'
    name = fields.Char('Name',required=True)
    code= fields.Char('Code',required=True)
    image_medium = fields.Binary(
        "Medium-sized image")
    internal_notes = fields.Text('Internal Notes')
    terms_condition = fields.Text('Terms and Condition')
    valid_from = fields.Date('Valid From',default=fields.Date.today())
    valid_till = fields.Date('Valid Till',default=fields.Date.today())
    seasons = fields.Selection([('peak','Peak'),('high','High'),('medium','Medium'),('low','Low')])
    minimum_stay = fields.Integer('Minimum Stay',required=True)
    maximum_stay = fields.Integer('Maximum Stay',required=True)
    price = fields.Float('Price',required=True)
    additional_person_charge = fields.Float('Additional Person Charge')
    additional_child_charge = fields.Float('Additional Child Charge')
    additional_infant_charge = fields.Float('Additional Infant Charge')
    default_duration = fields.Date('Date')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
    booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
    booking_source = fields.Many2many('ba.booking.source',string='Booking Source')
    room_type = fields.Many2one('ba.room.type',required=True)
    status = fields.Boolean(string='Status')
    scalable = fields.Char('Scalable')
    extend_stay_type = fields.Selection([('prorata','Prorata'),('double','Double')])
    fixed_start_date = fields.Date('Start Date', required=True, default=fields.Date.today())
    fixed_end_date  = fields.Date('End Date', required=True, default= fields.Date.today())


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
class BaCancellationPolicy(models.Model):
    _name = 'ba.cancellation.policies'
    _description = 'Cancellation Policy'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    days_before_arrival = fields.Integer('Days Before Arrival',required=True)
    cancellation_charges_in = fields.Selection([('fixed_amounnt','Fixed Amount'),('percentage','Percentage'),('room_night','Room Night')])
    chagre = fields.Float('Cancellation Charge',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    status = fields.Boolean('Active?',required=True)
class BaBookingPolicy(models.Model):
    _name = 'ba.booking.policies'
    _description = 'Booking Policy'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    days_before_arrival = fields.Integer('Days Before Arrival',required=True)
    chagre = fields.Float('Cancellation Charge',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    status = fields.Boolean('Active?',required=True)
    package = fields.Many2many('ba.packages',string='Packages')
    rate_type = fields.Many2many('ba.rate.type',required=True)
class BaGroupBooking(models.Model):
    _name = 'ba.group.booking'
    _description = 'Group Booking'
    name = fields.Char('Name',required=True)
    start_date = fields.Date('Start Date',required=True,default = fields.Date.today())
    end_date = fields.Date('End Date',required=True,default = fields.Date.today())
    room_type= fields.Many2many('ba.room.type',string='Room Type')
    rate_type = fields.Many2many('ba.rate.type',string='Rate Type')
    customer = fields.Many2many('res.partner',string='Customer')
    package = fields.Many2many('ba.packages',string='Packages')
    booking_source = fields.Many2one('ba.booking.source',required=True)
    adults = fields.Integer('Adults',required=True)
    children = fields.Integer('Children',required=True)
    infants = fields.Integer('Infants',required=True)
class BaBookingSourceCategory(models.Model):
	_name= 'ba.booking.source.category'
	_description='Booking Source Category'
	name=fields.Char('Name',required=True)
	code = fields.Char('Code',required=True)
	booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
	cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
	rate_type = fields.Many2one('ba.rate.type',string='Rate Type')
	package  = fields.Many2many('ba.packages',string='Package')
class BaBookingSource(models.Model):
    _name = 'ba.booking.source' 
    _description = 'Booking Source'
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    valid_from = fields.Date('Valid From',required=True,default = fields.Date.today())
    valid_to = fields.Date('Valid To',required=True,default = fields.Date.today())
    booking_policies  = fields.Many2one('ba.booking.policies',string='Booking Policies')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policies')
    booking_type = fields.Selection([('direct_booking','Direct Booking'),('ota','OTA'),('walkin','Walkin'),('corporate_travel_agent','Corporate Travel Agent')])
    rate_type = fields.Many2one('ba.rate.type',string='Rate Type')
    package = fields.Many2many('ba.packages',string='Package')
    booking_source_category = fields.Many2one('ba.booking.source.category',string='Booking Source Category')
    @api.onchange('booking_source_category')
    def onchage_booking_source_category(self):
    	self.booking_policies = self.booking_source_category.booking_policies
    	self.cancellation_policies = self.booking_source_category.cancellation_policies
    	self.rate_type = self.booking_source_category.rate_type
    	self.package = self.booking_source_category.package

        
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
    paid_status = fields.Boolean('Paid')
    reservation_status = fields.Selection([('tentative','Tentative'),('confirmed','Confirmed'),('no_show','  No Show'),('checked_in','Checked In')])
    amount = fields.Float('Amount')
    booking_policies = fields.Many2one('ba.booking.policies',string='Booking Policies')
    cancellation_policies = fields.Many2one('ba.cancellation.policies',string='Cancellation Policy')
    reservation_line = fields.One2many('ba.reservation.line','reservation_id',string='Reservation Line')

    @api.model
    def create(self,values):
        rec = super(BaReservation, self).create(values)
        print(rec)
        sale_order = self.env['sale.order'].create({
            'date_order':values['booking_date'],
            'partner_id':values['customer'],
            'amount_total':values['amount']
            

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
            

    
class BaReservationLine(models.Model):
    _name = 'ba.reservation.line'
    _description ='Reservation line'
    reservation_id = fields.Many2one('ba.reservation','Reservation Reference', ondelete='cascade')
    room_type_line = fields.Many2one('ba.room.type','Room Type')
    room_cost = fields.Float('Price')
    quantity = fields.Integer('Quantity', default=1)
    customer = fields.Many2one('res.partner',string='Customer')
    package = fields.Many2one('ba.packages',string='Package')
    arrival_date = fields.Date('Arrival Date',required=True,default= fields.Date.today())
    departure_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    booking_date = fields.Date('Departure Date',required=True,default= fields.Date.today())
    @api.onchange('booking_date')
    def set_customers(self):
        print(self.reservation_id.customer)
        if self.reservation_id.customer:
            self.customer = self.reservation_id.customer
        else:
            pass
        if self.reservation_id.arrival_date:
            self.arrival_date = self.reservation_id.arrival_date
        else:
            pass
        if self.reservation_id.departure_date:
            self.departure_date = self.reservation_id.departure_date
        else:
            pass

            
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


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _name= 'ba.partner'







