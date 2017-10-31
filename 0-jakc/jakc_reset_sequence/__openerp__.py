# -*- coding: utf-8 -*-

{
    'name': 'Jakc Labs - Reset Sequence',
    'version': '8.0.0.1.0',
    'category': 'General',
    'license': 'AGPL-3',
    'summary': 'Reset Sequence Number for SO, PO and Invoice',
    'author': "Jakc Labs,Odoo Community Association (OCA)",
    'website': 'http://www.jakc-labs.com/',
    'depends': [
        'account','sale','purchase'
    ],
    'data': [
        'jakc_reset_sequence_scheduler.xml',
    ],
    'installable': True,
    'application': True,
}
