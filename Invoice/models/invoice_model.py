# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from num2words import num2words
from math import ceil

class customer(models.Model):
    _name = 'customer.table'
    _description = 'Customer details'
    name = fields.Char('Customer Name', required=True,size=50)
    address = fields.Text('Address' )
    phone = fields.Char('Phone',size=15)
    saletax_no = fields.Char('SaleTax Number')
    ntn_no = fields.Char('NTN Number')


    _sql_constraints = [
                 ('name_unique', 'unique (name)', 'Name already exists...!'),
                 ('NTN_no_unique', 'unique (ntn_no)', 'NTN_no already exists...!'),
                 ('SaleTax_no_unique', 'unique (saletax_no)', 'SaleTax_no already exists...!')
                 ]


class company(models.Model):
    _name = 'company.table'
    _description = 'Company details'
    name = fields.Char('Company Name', required=True,size=50)
    address = fields.Text('Address')

    phone = fields.Char('Phone',size=15)
    saletax_no = fields.Char('SaleTax Number')
    ntn_no = fields.Char('NTN Number')
    cm_no=fields.Integer('Cash Memo Serial No.')
    csv_no=fields.Integer('Credit Sale Voucher Serial No.')
    ci_no=fields.Integer('Commercial Invoice Serial No.')
    dc_no=fields.Integer('Delivery Challan Serial No.')
    sti_no=fields.Integer('Sales Tax Invoice Serial No.')

    _sql_constraints = [
                 ('name_unique', 'unique (name)', 'Name already exists...!'),
                 ('NTN_no_unique', 'unique (ntn_no)', 'NTN_no already exists...!'),
                 ('SaleTax_no_unique', 'unique (saletax_no)', 'SaleTax_no already exists...!')
                 ]

# class cashMemo(models.Model):
#     _name = 'cashmemo.table'
#     _description = 'Table for Cash Memo'
#     name = fields.Integer('Invoice No.')
#     item = fields.Many2many('invoiceproduct.table',
#         ondelete='set null', string="Item", index=True)
#     cmpny_id =  fields.Many2one('company.table',
#         ondelete='set null', string="Company", index=True)
#     cst_id =  fields.Many2one('customer.table',
#         ondelete='set null', string="Customer", index=True)
#
#     _sql_constraints = [
#                  ('name_unique', 'unique (name)', 'Invoice No. already exists...!')
#                  ]
#
class invoiceProduct(models.Model):
    _name = 'invoiceproduct.table'
    _description = 'Table for Invoice Products names/description'
    name = fields.Char('Item', required="1")


class InvoiceHeader(models.Model):
    _name = 'invoiceheader.table'
    _description = 'Common table for all invoice Headers'
    name = fields.Char('Ref No')
    cmpny_id =  fields.Many2one('company.table',
            ondelete='set null', string="Company", index=True)
    cst_id =  fields.Many2one('customer.table',
            ondelete='set null', string="Customer", index=True)

    date = fields.Date('Date')
    po_dated = fields.Date('PO Dated')
    memotype = fields.Char('Memo Type')
    hs_code = fields.Char('HS Code')
    discount = fields.Integer('Discount',default=0)
    discount_amnt = fields.Float('Discount Amount')
    advance_amnt = fields.Float('Advance Amount')
    cp = fields.Char('Contact Person',size=15)
    fu = fields.Char('Follow Up',size=15)
    through = fields.Char('Through')
    cp_phn = fields.Char('CP Phone#',size=15)
    fu_phn = fields.Char('FU Phone#',size=15)
    invoice_name =fields.Char('No.')
    po = fields.Char('PO Number')
    dc = fields.Char('DC Number')
    dc_dated = fields.Date('DC Dated')
    term_sale = fields.Char('Terms of Sale')
    time_supply = fields.Char('Time of Supply')
    advance = fields.Integer('Advance Payment')
    balance = fields.Float('Remaining Balance')
    sub_ttl = fields.Float('Sub Total')
    tax_amnt = fields.Float('Tax Amount')
    sed_amnt = fields.Float('SED Amount')
    tax = fields.Boolean('Sale Tax',default=False)
    amnt_in_words = fields.Char('Amount in words')
    total = fields.Float('Total')
    exclude_st_sed = fields.Float('Amount Excluding S.T & S.E.D. Rs. P')
    current_date = fields.Date(default=fields.Date.today)
    sales_tax = fields.Float('Sales Tax @ 17% Rs. P')
    include_st_sed = fields.Float('Amount Including S.T & S.E.D. Rs. P')
    sed = fields.Float('S.E.D @_% Rs. P')
    item_size = fields.Integer('No of items')
    item = fields.One2many('invoicedetails.table','relation',
            ondelete='set null', string="Item", index=True)
    discount_type = fields.Selection([
        ('Flat', 'Flat'),
        ('Percent', 'Percent')], string='Discount Type',default='Flat')
    status = fields.Selection([
        ('Active', 'Active'),
        ('Inactive', 'Inactive')], string='Status',default='Active')
    view = fields.Boolean(compute='_check')

    _sql_constraints = [('name_unique', 'unique (name,cmpny_id)', 'Ref No already exists...!')]


    # @api.one
    # #@api.depends('name')
    # def amount_all(self):
    #     records = self.env['invoiceheader.table'].search([('memotype','=',self.memotype)])
    #     sum = 0
    #     for val in records:
    #         sum += val.total
    #     self.view_total = sum

    @api.multi
    @api.depends('item')
    def _check(self):
        if len(self.item)>0:
            self.view=True
        else:
            self.view=False

    def add_zeros(self, a):
        if(len(str(a))==1):
            return '00000'+str(a)
        elif(len(str(a))==2):
            return '0000'+str(a)
        elif(len(str(a))==3):
            return '000'+str(a)
        elif(len(str(a))==4):
            return '00'+str(a)
        elif(len(str(a))==5):
            return '0'+str(a)
        else:
            return str(a)





    @api.onchange('cmpny_id')
    def ref_no(self):
        if self.memotype == 'creditsalevoucher':
            self.name='CR-'+self.add_zeros(self.cmpny_id.csv_no)
        elif self.memotype == 'cashmemo':
            self.name='CM-'+self.add_zeros(self.cmpny_id.cm_no)
        elif self.memotype == 'deliverychallan':
            self.name='DC-'+self.add_zeros(self.cmpny_id.dc_no)
        elif self.memotype=='commercialinvoice':
            self.name='CI-'+self.add_zeros(self.cmpny_id.ci_no)
        elif self.memotype=='salestaxinvoice':
            self.name=self.add_zeros(self.cmpny_id.sti_no)

    @api.onchange('discount')
    def check_discount(self):
        if self.discount<0:
            raise UserError('Discount cannot be negative')

    def calculate_Total(self):
        self.item_size=len(self.item)
        self.total = 0;
        self.sub_ttl = 0
        self.discount_amnt = 0
        self.balance = 0
        self.tax_amnt = 0
        self.include_st_sed = 0
        self.exclude_st_sed = 0
        self.sales_tax = 0
        self.sed = 0

        for val in self.item:
            self.sub_ttl += val.amount
        if self.memotype == 'creditsalevoucher':
            if self.discount_type == 'Percent':
                if self.discount:
                    if self.discount<0:
                        raise UserError('Discount cannot be negative')
                    else:
                        self.discount_amnt = ceil(self.sub_ttl*(self.discount)/100)
            elif self.discount_type == 'Flat':
                if self.discount:
                    if self.discount<0:
                        raise UserError('Discount cannot be negative')
                    else:
                        self.discount_amnt = self.discount
            else:
                raise UserError('Please Select discount type')
            self.total = self.sub_ttl - self.discount_amnt
            if self.advance:
                if self.advance<0:
                    raise UserError('Advance Amount cannot be negative')
                else:
                    self.advance_amnt = self.advance
                    self.balance = self.total - self.advance
            else:
                self.balance = self.total
        elif self.memotype == 'cashmemo':
            if self.discount_type == 'Percent':
                if self.discount:
                    if self.discount<0:
                        raise UserError('Discount cannot be negative')
                    else:
                        self.discount_amnt = ceil(self.sub_ttl*(self.discount)/100)
            elif self.discount_type == 'Flat':
                if self.discount:
                    if self.discount<0:
                        raise UserError('Discount cannot be negative')
                    else:
                        self.discount_amnt = ceil(self.discount)
            else:
                raise UserError('Please Select discount type')
            self.total = float("{:.2f}".format(self.sub_ttl - self.discount_amnt))
        elif self.memotype == 'deliverychallan':
            if self.tax == 1:
                self.tax_amnt = ceil(self.sub_ttl*0.17)
            self.total = float("{:.2f}".format(self.sub_ttl - self.discount_amnt + self.tax_amnt))
        elif self.memotype=='commercialinvoice':
            if self.tax == 1:
                self.tax_amnt=self.sub_ttl*0.17
            self.total=float("{:.2f}".format(self.sub_ttl+self.tax_amnt))
        elif self.memotype=='salestaxinvoice':
            for val in self.item:
                self.include_st_sed += ceil(val.include_st_sed)
                self.exclude_st_sed += ceil(val.amount)
                self.sales_tax += ceil(val.sales_tax)
                self.sed += ceil(val.sed)
        else:
            for val in self.item:
                self.total += float("{:.2f}".format(val.amount))
        if self.memotype == 'creditsalevoucher':
            self.amnt_in_words = num2words(self.balance)
        else:
            self.amnt_in_words = num2words(self.total)



    @api.constrains('date','po_dated','dc_dated','status')
    def check_date(self):
        if(self.date):
            if(self.date>self.current_date):
                raise UserError("Future Date can't be selected")
        if(self.po_dated):
            if(self.po_dated>self.current_date):
                raise UserError("Future PO Date can't be selected")
        if(self.dc_dated):
            if(self.dc_dated>self.current_date):
                raise UserError("Future DC Dated can't be selected")
        if self.view==False:
            raise UserError('Please add atleast 1 item to save the invoice')
        if self.status !='Active' and self.status !='Inactive':
            raise UserError('Please Select Invoice status')

    @api.constrains('item','discount','advance','discount_type','tax')
    def check_save(self):
        self.calculate_Total()


    @api.constrains('cmpny_id')
    def test(self):
        if self.memotype == 'creditsalevoucher':
            self.name='CR-'+ self.add_zeros(self.cmpny_id.csv_no)
            self.cmpny_id.csv_no+=1
        elif self.memotype == 'cashmemo':
            self.name='CM-'+ self.add_zeros(self.cmpny_id.cm_no)
            self.cmpny_id.cm_no+=1
        elif self.memotype == 'deliverychallan':
            self.name='DC-'+ self.add_zeros(self.cmpny_id.dc_no)
            self.cmpny_id.dc_no+=1
        elif self.memotype=='commercialinvoice':
            #self.name='CI-'+ self.add_zeros(self.cmpny_id.ci_no)
            self.cmpny_id.ci_no+=1
        elif self.memotype=='salestaxinvoice':
            #self.name= self.add_zeros(self.cmpny_id.sti_no)
            self.cmpny_id.sti_no+=1

    @api.multi
    def generate_invoice(self):
        self.ensure_one()
        formview_id = self.env.ref('Invoice.view_form_withoutDc_task').id
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'invoiceheader.table',
        'view_type': 'form',
        'view_mode': 'form',
        'views': [(formview_id, 'form')],
        'target': 'new',
        'context': {'default_cst_id': self.cst_id.id,'default_cmpny_id': self.cmpny_id.id,'default_date': self.date,'default_po': self.po,'default_po_dated': self.po_dated,'default_memotype':self.memotype,'default_dc':self.cmpny_id.dc_no,'default_dc_dated':self.dc_dated}
        }

class InvoiceDetails(models.Model):
    _name = 'invoicedetails.table'
    _description = 'Common table for invoice details including Product details like Amount etc.'
    name = fields.Many2one('invoiceproduct.table',
             ondelete='set null', string="Item", index=True)
    relation = fields.Many2one('invoiceheader.table',
             ondelete='set null', string="Item", index=True)
    qty = fields.Integer('Product Quantity',default=0)
    item_description = fields.Text(string="Item Description")
    rate = fields.Float('Product Rate',default=0)
    amount = fields.Float('Product Amount')
    sub_ttl = fields.Integer('Sub Total')
    tax_amnt = fields.Float('Tax Amount')
    sed_amnt = fields.Float('SED Amount')
    sed = fields.Float('S.E.D @_% Rs. P')
    exclude_st_sed = fields.Float('Amount Excluding S.T & S.E.D. Rs. P')
    sales_tax = fields.Float('Sales Tax @ 17% Rs. P')
    include_st_sed = fields.Float('Amount Including S.T & S.E.D. Rs. P')
    type = fields.Char('type')

    @api.onchange('item_description')
    def _check_your_field(self):
        if self.item_description:
            if len(self.item_description) > 150:
                raise ValidationError('Number of characters must on exceed 150')

    @api.onchange('qty','rate')
    def check_qty_rate(self):
        if(self.qty<0):
            raise UserError("Negative quantity can't be added")
        if(self.rate<0):
            raise UserError("Negative rate can't be added")

    @api.constrains('qty','rate')
    def calculate_amount(self):
        if(self.qty==0):
            raise UserError("Zero quantity can't be added")
        elif(self.rate==0 and self.relation.memotype!='deliverychallan'):
            raise UserError("Zero rate can't be added")
        elif(self.qty<0):
            raise UserError("Negative quantity can't be added")
        elif(self.rate<0):
            raise UserError("Negative rate can't be added")
        self.amount = float("{:.2f}".format(self.qty * self.rate))
        self.sales_tax=ceil(self.amount *0.17)
        self.include_st_sed=ceil(self.amount+self.sales_tax+self.sed)




class commercialinvoicewithdc(models.Model):
    _name = 'commercialinvoicewithdc.table'
    _description = 'Table '
    name = fields.Char('Name')
    dc = fields.Many2one('invoiceheader.table',
             ondelete='set null', string="Delivery Challan", index=True)
    dc_no = fields.Integer('DC Number')
    invoice_name =fields.Char('No.',default="CINV-00000111")
    memotype = fields.Char('Memo Type',default="withdc")
    customer = fields.Char(related='dc.cst_id.name')
    company = fields.Char(related='dc.cmpny_id.name')

    @api.onchange('dc')
    def filter_dc(self):
        # domain = [('memotype', '=', 'deliverychallan')]
        # dones = self.env['invoiceheader.table'].search(domain)
        return {'domain': {'dc': [('memotype', '=', 'deliverychallan')]}}

    @api.constrains('dc')
    def set_dc_no(self):
        self.dc.tax_amnt = 0
        self.dc.total = 0
        for val in self.dc.item:
            self.dc.tax_amnt += val.amount*0.17
        self.dc.total += self.dc.tax_amnt
        self.dc_no = self.dc.id
