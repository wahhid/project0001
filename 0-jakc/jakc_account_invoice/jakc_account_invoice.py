import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def Terbilang(self, x):
        angka = {1: 'Satu', 2: 'Dua', 3: 'Tiga', 4: 'Empat', 5: 'Lima', 6: 'Enam', 7: 'Tujuh', 8: 'Delapan',
                 9: 'Sembilan'}
        b = ' Puluh '
        c = ' Ratus '
        d = ' Ribu '
        e = ' Juta '
        f = ' Miliyar '
        g = ' Triliun '

        y = x
        n = len(y)
        if n <= 3:
            if n == 1:
                if y == '0':
                    return ''
                else:
                    return angka[int(y)]
            elif n == 2:
                if y[0] == '1':
                    if y[1] == '1':
                        return 'Sebelas'
                    elif y[0] == '0':
                        x = y[1]
                        return self.Terbilang(x)
                    elif y[1] == '0':
                        return 'Sepuluh'
                    else:
                        return angka[int(y[1])] + ' Belas'
                elif y[0] == '0':
                    x = y[1]
                    return self.Terbilang(x)
                else:
                    x = y[1]
                    return angka[int(y[0])] + b + self.Terbilang(x)
            else:
                if y[0] == '1':
                    x = y[1:]
                    return 'Seratus ' + self.Terbilang(x)
                elif y[0] == '0':
                    x = y[1:]
                    return self.Terbilang(x)
                else:
                    x = y[1:]
                    return angka[int(y[0])] + c + self.Terbilang(x)
        elif 3 < n <= 6:
            p = y[-3:]
            q = y[:-3]
            if q == '1':
                return 'Seribu' + self.Terbilang(p)
            elif q == '000':
                return self.Terbilang
            return self.Terbilang(q) + d + self.Terbilang(p)
        elif 6 < n <= 9:
            r = y[-6:]
            s = y[:-6]
            return self.Terbilang(s) + e + self.Terbilang(r)
        elif 9 < n <= 12:
            t = y[-9:]
            u = y[:-9]
            return self.Terbilang(u) + f + self.Terbilang(t)
        else:
            v = y[-12:]
            w = y[:-12]
            return self.Terbilang(w) + g + self.Terbilang(v)

    def get_terbilang(self, cr, uid, ids, field_name, arg, context=None):
        invoice = self.browse(cr, uid, ids[0], context=context)
        terbilang = self.Terbilang(str(int(invoice.amount_total)))
        x = {}
        x[ids[0]] = terbilang
        return x

    _columns = {
        'terbilang' : fields.function(get_terbilang, type='char', method=True, string='Terbilang'),
        'printed_number': fields.integer('Printed #', readonly=True),
        'payment_method': fields.char('Payment Method'),
    }

    _defaults ={
        'printed_number': lambda *a: 0,
        'date_invoice': datetime.today().strftime('%Y-%m-%d'),
    }

    def add_print_count(self, cr, uid, invoice, context=None):
        print_count = invoice.printed_number + 1
        values = {}
        values.update({'printed_number': print_count})
        self.pool.get('account.invoice').write(cr, uid, [invoice.id], values, context=context)
        return True



    def print_receipt(self, cr, uid, ids, context=None):
        invoice = self.pool.get('account.invoice').browse(cr, uid, ids[0], context=context)
        self.add_print_count(cr, uid, invoice, context=context)
        terbilang = self.Terbilang(str(invoice.amount_total)[:-2])
        serverUrl = 'http://103.252.101.243:8080/jasperserver'
        j_username = 'jasperadmin'
        j_password = 'pelang1'
        ParentFolderUri = '/reports/bcp'
        reportUnit = '/reports/bcp/nota_penjualan'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&decorate=no&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&decorate=no&NUMBER=' + invoice.number + '&TERBILANG=' + terbilang +'&j_username=' + j_username + '&j_password=' + j_password
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new'
        }


