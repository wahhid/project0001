from itertools import chain
import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import except_orm

import openerp.addons.decimal_precision as dp

class ProductPriceslistItem(osv.osv):
    _inherit = 'product.pricelist.item'

    _columns = {
        'partner_type_id': fields.many2one('res.partner.type', 'Partner Type')
    }


