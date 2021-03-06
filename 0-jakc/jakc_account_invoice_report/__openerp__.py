{
    'name' : 'Jakc Labs - Account Invoice Report Enhancement',
    'version' : '1.0',
    'author' : 'Jakc Labs',
    'category' : 'Generic Modules/Account Invoice',
    'depends' : ['account','account_invoice_production_lot', 'jakc_account_invoice'],
    'init_xml' : [],
    'data' : [
        'views/report_view.xml',
        'views/res_company_view.xml',
        'jakc_account_invoice_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}