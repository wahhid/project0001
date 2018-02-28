{
    'name' : 'Sale Report',
    'version' : '1.0',
    'author' : 'Jakc Labs',
    'category' : 'Generic Modules/Sale',
    'depends' : ['sale'],
    'init_xml' : [],
    'data' : [
        'wizards/sale_report_view.xml',
        'views/sale_report_menu.xml',
        'reports/report_customer_sale_summary_view.xml',
        'reports/report_customer_sale_summary.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}