# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.sql import drop_view_if_exists

class report_stock_quant(osv.osv):
    _name = "report.stock.quant"
    _auto = False
    _rec_name = "product_id"
    _order = "product_id"
    _columns = {
        'id': fields.integer('id', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'lot_id': fields.many2one('stock.production.lot', 'Lot', readonly=True),
        'qty': fields.float('Quantity', readonly=True),
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'report_stock_quant')
        cr.execute("""
            create or replace view report_stock_quant as (
                select
                ROW_NUMBER() OVER (ORDER BY p.product_id ASC) AS id,
                p.product_id as product_id,
                p.lot_id as lot_id,
                sum(p.qty) as qty
            from
                stock_quant p
                group by p.product_id, p.lot_id
            )""")
