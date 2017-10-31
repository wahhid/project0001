import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp


class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    _columns = {
        'iface_cheque': fields.boolean('Cheque'),
        'cheque_number': fields.char('Cheque #', size=20),
        'cheque_due_date': fields.date('Cheque Due Date'),
    }

    defaults = {
        'iface_cheque': lambda *a : False,
    }