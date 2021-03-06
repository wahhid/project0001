from openerp.osv import fields, osv
from datetime import datetime
import logging
import urllib

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('all','All'),
    ('done','Done Only')
]

class inventory_report(osv.osv_memory):
    _name = "inventory.report"
    _columns = {
        'report_id': fields.selection([
            ('01', 'Laporan Inventory Per Merek'),

        ], 'Report Name'),
        'product_merk_id': fields.many2one('product.merk','Merk'),
        'start_date': fields.date('Start Date'),
    }

    _defaults = {
        'report_id': lambda *a: '01',
        'start_date': fields.date.context_today,
    }




    def generate_report(self, cr, uid, ids, context=None):
        params = self.browse(cr, uid, ids, context=context)
        param = params[0]
        if param.report_id == '01':
            serverUrl = 'http://103.252.101.243:8080/jasperserver'
            j_username = 'jasperadmin'
            j_password = 'pelang1'
            ParentFolderUri = '/reports/bcp'
            reportUnit = '/reports/bcp/Laporan_Rekap_Penjualan'
            url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&decorate=no&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&decorate=no&START_DATE=' + param.start_date + '&END_DATE=' + param.end_date + '&j_username=' + j_username + '&j_password=' + j_password
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'
            }
        if param.report_id == '02':
            serverUrl = 'http://103.252.101.243:8080/jasperserver'
            j_username = 'jasperadmin'
            j_password = 'pelang1'
            ParentFolderUri = '/reports/bcp'
            reportUnit = '/reports/bcp/laporan_penjualan_detail'
            url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&decorate=no&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&decorate=no&START_DATE=' + param.start_date + '&END_DATE=' + param.end_date + '&j_username=' + j_username + '&j_password=' + j_password
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'
            }
        if param.report_id == '03':
            serverUrl = 'http://103.252.101.243:8080/jasperserver'
            j_username = 'jasperadmin'
            j_password = 'pelang1'
            ParentFolderUri = '/reports/bcp'
            reportUnit = '/reports/bcp/laporan_penjualan_detail_by_sales'
            sales_ids = params.sales_ids
            list_sales = ''
            if sales_ids:
                for sales_id in sales_ids:
                    list_sales = str(sales_id.id) + ','
                list_sales = list_sales + '0'

            url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&decorate=no&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&decorate=no&START_DATE=' + param.start_date + '&END_DATE=' + param.end_date + '&LIST_SALES=' + list_sales  +'&j_username=' + j_username + '&j_password=' + j_password
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'
            }
