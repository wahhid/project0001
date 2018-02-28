from datetime import datetime, timedelta
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow


import logging

_logger = logging.getLogger(__name__)


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def get_access_for_amount_total(self, cr, uid, context=None):
        return self.pool.get('res.users').has_group(cr, uid, 'base.group_sale_store')

    _columns = {
        'iface_able_to_read_amount_total':fields.function(get_access_for_amount_total, type='boolean', string='Is user able to see amount product?')
    }
    #def action_wait(self, cr, uid, ids, context=None):
    #    sale_order_obj = self.pool.get('sale.order')
    #    sale_order = self.browse(cr, uid, ids[0], context=context)
    #    partner_id = sale_order.partner_id
    #    args = [('state','in',['progress','manual'])]
    #    sale_order_ids =  sale_order_obj.search(cr, uid, args, context=context)
    #    if sale_order_ids:
    #        raise osv.except_osv(_('Error!'), _('You cannot confirm a sales order because customer still have outstanding sale order or invoice.'))
    #    else:
    #        super(sale_order,self).action_wait(cr, uid, ids, context=context)
    #    return True

sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id,
                                                                       context=context)
        res['lot_id'] = line.lot_id.id
        _logger.info("Execute Prepare Order Line Invoice Line")
        return res

    _columns = {
        'product_uom_qty': fields.float('Qty', digits_compute= dp.get_precision('Product UoS'), required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'product_uom': fields.many2one('product.uom', 'Uom ', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    }

sale_order_line()


