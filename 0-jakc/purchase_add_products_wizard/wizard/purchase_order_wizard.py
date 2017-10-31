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
class purchase_order_add_multiple(models.TransientModel):
    _name = 'purchase.order.add_multiple'
    _description = 'Purchase order add multiple'

    quantity_type = fields.Selection(AVAILABLE_QUANTITY_TYPE,'Type', size=16, default='fixed')
    quantity = fields.Float('Quantity',
                            default='1.0')
    products_ids = fields.Many2many(
        'product.product',
        string='Products',
        domain=[('purchase_ok', '=', True)],
    )

    @api.one
    def add_multiple(self):
        active_id = self._context['active_id']
        sale = self.env['purchase.order'].browse(active_id)
        for product_id in self.products_ids:
            if self.quantity_type == 'fixed':
                qty = self.quantity
            else:
                cur_product  = self.env['product.template'].browse([product_id.product_tmpl_id.id])
                qty = cur_product.qty_available

            product = self.env['purchase.order.line'].product_id_change(
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
