# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import pytz
import time
from openerp import tools
from openerp.osv import osv
from openerp.report import report_sxw


class deposit_details(report_sxw.rml_parse):

    def _get_all_users(self):
        user_obj = self.pool.get('res.users')
        return user_obj.search(self.cr, self.uid, [])

    def _get_selected_partners(self, form):
        partner_obj = self.pool.get('res.partner')
        partner_args = [('id','in',form['partner_ids'])]
        partner_ids = partner_obj.search(self.cr, self.uid, partner_args)
        return partner_obj.browse(self.cr, self.uid, partner_ids,[])

    def _get_account_move_line(self, partner_id):
        data = []
        result = {}
        user_obj = self.pool.get('res.users')
        company = user_obj.browse(self.cr, self.uid, self.uid, []).company_id
        deposit_account_id = company.deposit_account_id.id
        account_move_line_obj = self.pool.get('account.move.line')
        account_move_line_args = [('partner_id','=',partner_id),('account_id','=',deposit_account_id)]
        account_move_line_ids = account_move_line_obj.search(self.cr, self.uid, account_move_line_args)
        account_move_lines = account_move_line_obj.browse(self.cr, self.uid, account_move_line_ids, [])
        for account_move_line in account_move_lines:
            result = {
                'debit': account_move_line.debit,
                'credit': account_move_line.credit,
            }
            data.append(result)
        if data:
            return data
        else:
            return {}

    def __init__(self, cr, uid, name, context=None):
        super(deposit_details, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'selected_partners': self._get_selected_partners,
            'account_move_lines': self._get_account_move_line,
        })


class report_jakc_cust_deposit(osv.AbstractModel):
    _name = 'report.report_cust_deposit'
    _inherit = 'report.abstract_report'
    _template = 'jakc_cust_deposit_report.report_custdeposit'
    _wrapped_report_class = deposit_details

