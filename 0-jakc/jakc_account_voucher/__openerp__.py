# -*- coding: utf-8 -*-
###############################################################################
#
#   account_check_deposit for Odoo
#   Copyright (C) 2012-2015 Akretion (http://www.akretion.com/)
#   @author: Benoît GUILLOT <benoit.guillot@akretion.com>
#   @author: Chafique DELLI <chafique.delli@akretion.com>
#   @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Jakc Labs - ',
    'version': '8.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Customer Deposit',
    'author': "Jakc Labs,Odoo Community Association (OCA)",
    'website': 'http://www.jakc-labs.com/',
    'depends': [
        'base','account',
    ],
    'data': [
        'jakc_cust_deposit_view.xml',
        'jakc_cust_deposit_menu.xml',
        'jakc_cust_deposit_sequence.xml',
    ],
    'installable': True,
    'application': True,
}
