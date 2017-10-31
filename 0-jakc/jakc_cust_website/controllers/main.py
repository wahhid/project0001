import logging
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp import tools
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

PPG = 20 # Products Per Page
PPR = 4  # Products Per Row

class bcp_shop(http.Controller):

    @http.route(['/bcp'], type='http', auth="user", website=True)
    def bcp_shop_website(self):
        values = {}
        return http.request.render("jakc_cust_website.bcp_shop", values)

    @http.route(['/bcp/products/page/<int:page>'], type='http', auth="user", website=True)
    def bcp_products_website(self, page=0, category=None, search='', ppg=False, **post):
        url = "/bcp/products"

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if search:
            domain = ['|', ('name', 'ilike', search), ('description', 'ilike', search)]
        else:
            domain = []

        if search:
            post["search"] = search

        product_count = http.request.env['product.template'].search(domain, count=True)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = http.request.env['product.template'].search(domain, limit=ppg, offset=pager['offset'])
        values = {
            'search': search,
            'pager': pager,
            'products': products,
        }
        return http.request.render('jakc_cust_website.bcp_shop_product', values)

    @http.route(['/bcp/product/detail/<int:product_id>'], type='http', auth="user", website=True)
    def bcp_product_detail(self, product_id):
        product = http.request.env['product.template'].browse(product_id)
        values = {
            'product': product
        }
        return http.request.render('jakc_cust_website.bcp_shop_product_detail', values)

    @http.route(['/bcp/cart/list'], type='http', auth='user', website=True)
    def bcp_product_cart(self):
        quotation_args = [('state', '=', 'draft')]
        quotation_ids = http.request.env['sale.order'].search(quotation_args)
        if quotation_ids:
            sale_order_id = quotation_ids[0]
        values = {
            'sale_order': sale_order_id
        }
        return http.request.render('jakc_cust_website.bcp_shop_cart_list', values)

    @http.route(['/bcp/cart/update/'], type='http', auth="user", website=True)
    def bcp_product_cart_update(self, product_id='', quantity='',  **post):
        quotation_args = [('state', '=', 'draft')]
        quotation_ids = http.request.env['sale.order'].search(quotation_args)
        if quotation_ids:
            sale_order_id = quotation_ids[0]
        values = {
            'sale_order': sale_order_id
        }
        return http.request.render('jakc_cust_website.bcp_shop_cart_list', values)
