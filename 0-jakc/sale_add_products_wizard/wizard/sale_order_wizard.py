# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


AVAILABLE_QUANTITY_TYPE = [
    ('manual', 'Manual Quantity'),
    ('fixed', 'Fixed Quantity'),
]
class sale_order_add_multiple(models.TransientModel):
    _name = 'sale.order.add_multiple'
    _description = 'Sale order add multiple'

    quantity_type = fields.Selection(AVAILABLE_QUANTITY_TYPE,'Type', size=16, default='fixed')
    quantity = fields.Float('Quantity',default='1.0')
    method_type = fields.Selection([('product','By Product'),('quant','By Stock Quant')], 'Type', default='product')
    products_ids = fields.Many2many(
        'product.product',
        string='Products',
        domain=[('sale_ok', '=', True)],
    )

    stock_quant_ids = fields.Many2many(
        'report.stock.quant',
        string='Stock Quant',
    )

    @api.one
    def add_multiple(self):
        active_id = self._context['active_id']
        sale = self.env['sale.order'].browse(active_id)

        if self.method_type == 'product':
            for product_id in self.products_ids:
                if self.quantity_type == 'fixed':
                    qty = self.quantity
                else:
                    cur_product  = self.env['product.template'].browse([product_id.product_tmpl_id.id])
                    qty = cur_product.qty_available

                product = self.env['sale.order.line'].product_id_change(
                    sale.pricelist_id.id,
                    product_id.id,
                    qty=qty,
                    uom=product_id.uom_id.id,
                    partner_id=sale.partner_id.id)
                val = {
                    'name': product['value'].get('name'),
                    'product_uom_qty': qty,
                    'order_id': active_id,
                    'product_id': product_id.id or False,
                    'product_uom': product_id.uom_id.id,
                    'price_unit': product['value'].get('price_unit'),
                    'tax_id': [(6, 0, product['value'].get('tax_id'))],
                }
                self.env['sale.order.line'].create(val)
        else:
            for stock_quant_id in self.stock_quant_ids:
                if self.quantity_type == 'fixed':
                    qty = self.quantity
                else:
                    #cur_product = self.env['product.template'].browse([stock_quant_id.product_id.product_tmpl_id.id])
                    qty = stock_quant_id.qty

                product = self.env['sale.order.line'].product_id_change(
                    sale.pricelist_id.id,
                    stock_quant_id.product_id.id,
                    qty=qty,
                    uom=stock_quant_id.product_id.uom_id.id,
                    partner_id=sale.partner_id.id)
                val = {
                    'name': product['value'].get('name'),
                    'lot_id': stock_quant_id.lot_id.id or False,
                    'product_uom_qty': qty,
                    'order_id': active_id,
                    'product_id': stock_quant_id.product_id.id or False,
                    'product_uom': stock_quant_id.product_id.uom_id.id,
                    'price_unit': product['value'].get('price_unit'),
                    'tax_id': [(6, 0, product['value'].get('tax_id'))],
                }
                self.env['sale.order.line'].create(val)