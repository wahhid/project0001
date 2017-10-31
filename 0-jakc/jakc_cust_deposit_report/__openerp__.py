# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Jakc Labs - Customer Deposit Report',
    'version': '1.0.1',
    'category': 'Customer Deposit',
    'author': 'Jakc Labs',
    'sequence': 20,
    'summary': 'Customer Deposit - Customer Deposit Report',
    'description': """
Customer Deposit - Customer Deposit Report
===============================
Customer Deposit - Customer Deposit Report
    """,
    'depends': ['jakc_cust_deposit'],
    'data': [
        'wizard/jakc_cust_deposit.xml',
        'views/report_cust_deposit.xml',
        'cust_deposit_report.xml',
    ],
    'installable': True,
    'application': True,
    'website': 'https://www.jakc-labs.com',
    'auto_install': False,
}
