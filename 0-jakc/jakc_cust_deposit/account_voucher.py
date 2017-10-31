import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp
import logging



_logger = logging.getLogger(__name__)

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    def _get_company(self, cr, uid, context=None):
        return self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id

    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None):

        res = super(account_voucher, self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=context)

        invoice_pool = self.pool.get('account.invoice')
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        company = self._get_company(cr, uid, context=context)

        if journal:
            company = self.pool.get('res.company').browse(cr, uid, company.id, context=context)
            if company.deposit_journal_id.id == journal.id:
                # Get Customer Deposit Amount
                if context.get('invoice_id', False):
                    invoice = invoice_pool.browse(cr, uid, context['invoice_id'], context=context)
                    if invoice.type == 'out_invoice':
                        sale_id = invoice.sale_ids[0]
                        deposit_id = sale_id.cust_deposit_id
                        res['value']['deposit'] = deposit_id.rest_amount
                        res['value']['cust_deposit_id'] = deposit_id.id
                    if invoice.type == 'out_refund':
                        res['value']['iface_deposit'] = True
                else:
                    res['value']['deposit'] = 0.0
            else:
                res['value']['deposit'] = 0.0

            if company.overpay_journal_id.id == journal.id:
                # Get Customer Overpay Amount
                if context.get('invoice_id', False):
                    invoice = invoice_pool.browse(cr, uid, context['invoice_id'], context=context)
                    if invoice.type == 'out_invoice':
                        sale_id = invoice.sale_ids[0]
                        partner_id  = sale_id.partner_id
                        res['value']['overpay'] = partner_id.overpay
                else:
                    res['value']['deposit'] = 0.0
            else:
                res['value']['deposit'] = 0.0

        return res


    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):

        vals = super(account_voucher, self).onchange_journal(cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=context)

        invoice_pool = self.pool.get('account.invoice')
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)

        if journal:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if company.deposit_journal_id.id == journal.id:
                #Get Customer Deposit Amount
                if context.get('invoice_id', False):
                    invoice = invoice_pool.browse(cr, uid, context['invoice_id'], context=context)
                    if invoice.type == 'out_invoice':
                        sale_id = invoice.sale_ids[0]
                        deposit_id = sale_id.cust_deposit_ids
                        vals['value']['deposit'] = deposit_id.rest_amount
                        vals['value']['cust_deposit_id'] = deposit_id.id

                    if invoice.type == 'out_refund':
                        vals['value']['iface_deposit'] = True
                else:
                    vals['value']['deposit'] = 0.0
            else:
                vals['value']['deposit'] = 0.0

            if company.overpay_journal_id.id == journal.id:
                # Get Customer Overpay Amount
                if context.get('invoice_id', False):
                    invoice = invoice_pool.browse(cr, uid, context['invoice_id'], context=context)
                    if invoice.type == 'out_invoice':
                        sale_id = invoice.sale_ids[0]
                        partner_id  = sale_id.partner_id
                        vals['value']['overpay'] = partner_id.overpay
                        if amount > partner_id.overpay:
                            vals['value']['amount']  = partner_id.overpay
                else:
                    vals['value']['deposit'] = 0.0
            else:
                vals['value']['deposit'] = 0.0

        return vals

    def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency,
                                   current_currency, context=None):
        '''
        Set a dict to be use to create the writeoff move line.

        :param voucher_id: Id of voucher what we are creating account_move.
        :param line_total: Amount remaining to be allocated on lines.
        :param move_id: Id of account move where this line will be added.
        :param name: Description of account move line.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: mapping between fieldname and value of account move line to create
        :rtype: dict
        '''

        _logger.warning('writeoff_move_line_get')
        currency_obj = self.pool.get('res.currency')
        move_line = {}

        voucher = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context)
        current_currency_obj = voucher.currency_id or voucher.journal_id.company_id.currency_id

        if not currency_obj.is_zero(cr, uid, current_currency_obj, line_total):
            diff = line_total
            account_id = False
            write_off_name = ''
            if voucher.payment_option == 'with_writeoff':
                _logger.warning('With Writeoff')
                account_id = voucher.writeoff_acc_id.id
                write_off_name = voucher.comment
            elif voucher.payment_option == 'deposit':
                _logger.warning('Deposit')
                company = self._get_company(cr, uid, context=context)
                account_id = company.deposit_account_id.id
                write_off_name = 'Customer Deposit'
            elif voucher.payment_option == 'overpay':
                _logger.warning('Overpay')
                company = self._get_company(cr, uid, context=context)
                account_id = company.overpay_account_id.id
                write_off_name = 'Overpay Deposit'
            elif voucher.partner_id:
                if voucher.type in ('sale', 'receipt'):
                    account_id = voucher.partner_id.property_account_receivable.id
                else:
                    account_id = voucher.partner_id.property_account_payable.id
            else:
                # fallback on account of voucher
                account_id = voucher.account_id.id
            sign = voucher.type == 'payment' and -1 or 1
            move_line = {
                'name': write_off_name or name,
                'account_id': account_id,
                'move_id': move_id,
                'partner_id': voucher.partner_id.id,
                'date': voucher.date,
                'credit': diff > 0 and diff or 0.0,
                'debit': diff < 0 and -diff or 0.0,
                'amount_currency': company_currency <> current_currency and (
                    sign * -1 * voucher.writeoff_amount) or 0.0,
                'currency_id': company_currency <> current_currency and current_currency or False,
                'analytic_account_id': voucher.analytic_id and voucher.analytic_id.id or False,
            }

        return move_line

    def button_proforma_voucher(self, cr, uid, ids, context=None):
        company = self._get_company(cr, uid, context=context)
        for voucher in self.browse(cr, uid, ids, context=context):
            _logger.info("Amount")
            _logger.info(voucher.amount)
            _logger.info("Overpay")
            _logger.info(voucher.partner_id.overpay)
            if company.overpay_journal_id.id == voucher.journal_id.id:
                if voucher.amount > voucher.partner_id.overpay:
                    raise osv.except_osv(_('Error!'), _('Cannot Process due Overpay Deposit not enough'))

        return super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)

    def account_move_get(self, cr, uid, voucher_id, context=None):
        _logger.warning('account_move_get')
        voucher = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context)
        move = super(account_voucher, self).account_move_get(cr, uid, voucher_id, context=context)
        _logger.warning(voucher.cust_deposit_id.id)
        move.update({'cust_deposit_id': voucher.cust_deposit_id.id})
        print move
        return move

    _columns = {
        'deposit': fields.float('Deposit Amount', readonly=True),
        'cust_deposit_id': fields.many2one('cust.deposit','Deposit', readonly=False),
        'iface_deposit': fields.boolean('Is Deposit', readonly=True),
        'overpay': fields.float('Overpay Amount', readonly=True),
        #'pricelist_id': fields.related('cust_deposit_id','pricelist_id', type="many2one", relation="product.pricelist", string="Pricelist", readonly=True),
        #'rest_amount': fields.related('cust_deposit_id','rest_amount', type="float", string="Rest Amount"),
        'payment_option': fields.selection([
            ('without_writeoff', 'Keep Open'),
            ('with_writeoff', 'Reconcile Payment Balance'),
            ('deposit', 'Deposit Account'),
            ('overpay', 'Overpay Account'),
        ], 'Payment Difference', required=True, readonly=True, states={'draft': [('readonly', False)]},
            help="This field helps you to choose what you want to do with the eventual difference between the paid amount and the sum of allocated amounts. You can either choose to keep open this difference on the partner's account, or reconcile it with the payment(s)"),
    }

    _defaults = {
        'iface_deposit': lambda *a: False,
    }