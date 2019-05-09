# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Inherit_Picking(models.Model):
    _inherit = "stock.picking"

    brand = fields.Many2one('brand.brand')
    
#     @api.onchange('picking_type_id')
#     def _picking_type_id(self):
#         operation_type = self.env.context.get('operation_type')
#         picking_type = self.env['stock.picking.type'].search([('name', 'ilike', operation_type)])
#         mlist = []
#         for val in picking_type:
#             mlist.append(val.id)
#         return {'domain': {'picking_type_id': [('id', 'in', mlist)]}}
    @api.multi
    def button_validate(self):
        self.ensure_one()
        
        stock = None
        no_quantities_done = all(line.qty_done == 0.0 for line in self.move_line_ids)
        if no_quantities_done:
            raise UserError(_('You cannot validate a transfer if you have not processed any quantity!!!.'))
        for val in self.move_line_ids:#.sorted(key=lambda m: m.product_id.id):
         #   if val.qty_done == 0:
            
            if self.picking_type_id.code == 'outgoing' or self.picking_type_id.code == 'internal':
                
                stock=self.env['stock.quant'].search([('product_id','=',val.product_id.id),('quantity','>',0),('location_id', '=', self.location_id.id)]).quantity
               
                if val.qty_done > stock:
                    raise UserError(' Available stock is less than quantity you entered (Available Stock: '+str(stock)+')\n for'+str(val.product_id.display_name))
        self.action_done()
        return
    
    @api.constrains('scheduled_date')
    def check_date(self):
        if(self.scheduled_date > self.date):
            raise UserError('You cannot pick a future date')
    

class brand(models.Model):
    _name = 'brand.brand'

    name = fields.Char('brand')


class InheritProductTemplate(models.Model):
    _inherit = "product.template"

    brand = fields.Many2one('brand.brand')
    categ_id = fields.Many2one(
        'product.category', 'Category',
        change_default=True, default='',
        required=True, help="Select category for the current product")
        
    mnfpno = fields.Char(string="Part No.")
    mnfCode = fields.Char(string="Model")
    
    @api.onchange('categ_id')
    def _productlist(self):
        if self.categ_id.id == 1 or self.categ_id.id == 2:
            raise UserError('This category is not allowed! kindly select another category')


class StockMove(models.Model):
    _inherit = "stock.move"
    
    qty_available = fields.Float('Quantity Available', compute='_compute_qty_available')
    mnfpno = fields.Char(string="Part No.", compute="_get_mnfpno_mnfcode_values")
    mnfCode = fields.Char(string="Model", compute="_get_mnfpno_mnfcode_values")
    product_category_id = fields.Many2one('product.category', "Category", compute="_get_mnfpno_mnfcode_values")
    
    @api.depends('product_id')
    def _compute_qty_available(self):
        for record in self:
            record.qty_available = record.product_id.qty_available
    
    @api.constrains('quantity_done')
    def _quantity_check(self):
        stock = 0
        
        if self.picking_type_id.code == 'outgoing' or self.picking_type_id.code == 'internal':
            #location_id = self.env['stock.picking.type'].browse(self.env.context.get('default_picking_type_id')).default_location_src_id.id
            products = self.env['product.product'].search([('product_tmpl_id', '=', 'defualt_product')])
            stock=self.env['stock.quant'].search([('product_id','=',self.product_id.id),('quantity','>',0),('location_id', '=', self.location_id.id)]).quantity
            #if location_id:
            #stock=self.env['stock.quant'].search([('product_id','=',self.product_id.id),('quantity','>',0),('location_id', '=', location_id)]).quantity
#                wt = self.env['stock.quant']
#                id_needed = wt.search([('product_id', '=',self.product_id.id),('quantity','>',0),('location_id', '=', location_id)]).quantity
#                new = wt.browse(id_needed)
#                list = [new.field1, new.field2, new.field3]
         #   if stock: 
           
            if self.quantity_done <= 0:
#                    return {
#                            'error': {
#                           'title': 'Stock is not available',
#                            'message': 'Available stock is minimum than done quantity you entered (Available Stock: '+str(stock)+')',
#                        },
#                    }
                raise UserError('- Negative or zero quantity not allowed')
            elif self.quantity_done > stock:
                 raise UserError('- Available stock is less than quantity you entered (Available Stock: '+str(stock)+')')
        else:
            if self.quantity_done <= 0:
                raise UserError('- Negative or zero quantity not allowed')
    
    @api.onchange('quantity_done')
    def _check(self):
        stock = 0
        
        if self.picking_type_id.code == 'outgoing' or self.picking_type_id.code == 'internal':
            #location_id = self.env['stock.picking.type'].browse(self.env.context.get('default_picking_type_id')).default_location_src_id.id
            products = self.env['product.product'].search([('product_tmpl_id', '=', 'defualt_product')])
            stock=self.env['stock.quant'].search([('product_id','=',self.product_id.id),('quantity','>',0),('location_id', '=', self.location_id.id)]).quantity
            #if location_id:
            #stock=self.env['stock.quant'].search([('product_id','=',self.product_id.id),('quantity','>',0),('location_id', '=', location_id)]).quantity
#                wt = self.env['stock.quant']
#                id_needed = wt.search([('product_id', '=',self.product_id.id),('quantity','>',0),('location_id', '=', location_id)]).quantity
#                new = wt.browse(id_needed)
#                list = [new.field1, new.field2, new.field3]
         #   if stock: 
           
            if self.quantity_done < 0:
#                    return {
#                            'error': {
#                           'title': 'Stock is not available',
#                            'message': 'Available stock is minimum than done quantity you entered (Available Stock: '+str(stock)+')',
#                        },
#                    }
                raise UserError('- Negative quantity not allowed')
            elif self.quantity_done > stock:
                 raise UserError('- Available stock is less than quantity you entered (Available Stock: '+str(stock)+')')
        else:
            if self.quantity_done < 0:
                raise UserError('- Negative quantity not allowed')
    

    
    
    @api.onchange('product_id')
    def _productlist_brand(self):
        mlist = []
        brand = self.env.context.get('default_brand')
        if self.picking_type_id.code == 'outgoing':
            location_id = self.env['stock.picking.type'].browse(self.env.context.get('default_picking_type_id')).default_location_src_id.id
        else:
            location_id = self.env.context.get('default_location_id')
        if brand:
            search_product_templates = self.env['product.template'].search([('brand', '=', brand)])
#             mlist = []
            if self.picking_type_id.code == 'incoming':
                for val in search_product_templates:
                    products = self.env['product.product'].search([('product_tmpl_id', '=', val.id)])
                    if len(products)>0:
                        for prod in products:
                            mlist.append(prod.id)
            else:
#                 for val in search_product_templates:
                reclist = [val.id for val in search_product_templates]
                products = self.env['product.product'].search([('product_tmpl_id', 'in', reclist)])
#                     if self.picking_type_id.code == 'incoming':
#                         stock=self.env['stock.quant'].search([('product_id','=',products.id)])
#                     if self.picking_type_id.code != 'incoming':
               # if products:
                #    stock=self.env['stock.quant'].search([('product_id','in',products.ids)])
               # if location_id:
               #     stock = stock.filtered(lambda a: a.quantity > 0 and a.location_id.id == location_id)
#                         stock=self.env['stock.quant'].search([('quantity','>',0),('location_id', '=', location_id)])
              #  else:
              #      stock = stock.filtered(lambda a: a.quantity > 0)
#                         stock=self.env['stock.quant'].search([('product_id','=',products.id),('quantity','>',0)])
              #  if len(stock)>0:
                for prod in products:
                    mlist.append(prod.id)
#                else:
#                    mlist.append(products.id)
#             return {'domain': {'product_id': [('id', 'in', mlist)]}}
#         raise UserError(_('Please select brand first'))
        return {'domain': {'product_id': [('id', 'in', mlist)]}}
    
    @api.one
    @api.depends('product_id')
    def _get_mnfpno_mnfcode_values(self):
        self.mnfpno = self.product_id.mnfpno
        self.mnfCode = self.product_id.mnfCode
        self.product_category_id = self.product_id.categ_id
