import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp


class res_partner(osv.osv):
    _inherit = 'res.partner'

    #def _compute_deposit_amount(self, cr, uid, ids, fields, arg, context=None):
    #    result = {}
    #    partner_id = ids[0]
    #    sql = """SELECT sum(credit - debit) as deposit FROM account_move_line WHERE partner_id=%s AND account_id=61"""
    #    cr.execute(sql, (partner_id,))
    #    result[partner_id] = cr.fetchone()[0]
    #   return result

    _columns = {
        'deposit': fields.function(_compute_deposit_amount, type='float', string='Deposit Amount', groups='account.group_account_invoice'),
    }


class res_partner_type(osv.osv):
    _name = 'res.partner.type'

    _columns = {
        'name': fields.char('Name', size=50)
    }

