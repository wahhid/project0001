from openerp import api, models, fields
from openerp.osv import osv
import openerp.addons.decimal_precision as dp


AVAILABLE_STATES = [
    ('draft','New'),
    ('open','Open'),
    ('done','Close'),
    ('cancel','Cancelled'),
]


class ResPartnerType(models.Model):
    _name = 'res.partner.type'

    @api.one
    def _generate_public_pricelist(self, version_id):
        print "Generate Public Pricelist"
        product_pricelist_item_obj = self.env['product.pricelist.item']
        vals = {}
        vals.update({'price_version_id': version_id})
        vals.update({'sequence': 99})
        vals.update({'base': 1})
        res = product_pricelist_item_obj.create(vals)

    @api.multi
    def _auto_create_pricelist(self, res):
        print "Auto Create Pricelist"
        pricelist_obj = self.env['product.pricelist']
        pricelist_version_obj = self.env['product.pricelist.version']

        pricelist_vals = {}
        pricelist_vals.update({'name': 'Pricelist - ' + res.name + ' Member'})
        pricelist_vals.update({'type': 'sale'})
        pricelist_id = pricelist_obj.create(pricelist_vals)

        vals = {}
        vals.update({'name': res.name + ' -  Member Version'})
        vals.update({'pricelist_id': pricelist_id.id})
        pricelist_version_id = pricelist_version_obj.create(vals)

        return pricelist_id

    @api.multi
    def trans_confirm(self):
        pricelist_id = self.pricelist_id
        version_id = pricelist_id.version_id[0]
        self._generate_public_pricelist(version_id.id)
        self.write({'state': 'open'})

    name = fields.Char('Name', size=100, required=True)
    discount = fields.Float('Discount', required=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly=True)
    partner_type_product_ids = fields.One2many('res.partner.type.product', 'partner_type_id','Products')
    state =  fields.Selection(AVAILABLE_STATES, 'Status', default='draft', readonly=True)

    @api.model
    def create(self, vals):
        res = super(ResPartnerType, self).create(vals)
        pricelist_id = self._auto_create_pricelist(res)
        res.update({'pricelist_id': pricelist_id.id})
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartnerType, self).write(vals)
        partner_type = self.browse(self.id)
        if 'discount' in vals:
            for product in partner_type.partner_type_product_ids:
                product.product_pricelist_item_id.price_discount = -1 * (partner_type.discount / 100)
        return True

    @api.multi
    def unlink(self):
        self.pricelist_id.unlink()
        res = super(ResPartnerType, self).unlink()
        return res

class ResPartnerTypeProduct(osv.osv):
    _name = 'res.partner.type.product'

    def _get_product(self, product_id):
        product_template_obj = self.env['product.template']
        product_template = product_template_obj.browse(product_id)
        return product_template

    def _get_product_category(self, product_id):
        product_category_obj = self.env['product.category']
        product_category = product_category_obj.browse(product_id)
        return product_category

    def _get_product_merk(self, product_id):
        product_merk_obj = self.env['product.merk']
        product_merk = product_merk_obj.browse(product_id)
        return product_merk

    def _add_product_version(self, partner_type_product):
        partner_type_obj = self.env['res.partner.type']
        partner_type_product_obj = self.env['res.partner.type.product']
        product_pricelist_item_obj = self.env['product.pricelist.item']

        partner_type = partner_type_product.partner_type_id

        if partner_type.pricelist_id.version_id[0].items_id:
            i = len(partner_type.pricelist_id.version_id[0].items_id) + 1
        else:
            i = 1
        version_id = partner_type.pricelist_id.version_id[0]
        vals = {}
        vals.update({'price_version_id': version_id.id})
        vals.update({'sequence': i})
        if partner_type_product.type == 'product':
            vals.update({'name': partner_type_product.product_id.name})
            vals.update({'product_id': partner_type_product.product_id.product_id.id})
        if partner_type_product.type == 'category':
            vals.update({'name': partner_type_product.product_category_id.name})
            vals.update({'categ_id': partner_type_product.product_category_id.id})
        if partner_type_product.type == 'merk':
            vals.update({'name': partner_type_product.product_merk_id.name})
            vals.update({'product_merk_id': partner_type_product.product_merk_id.id})
        vals.update({'base': 1})
        vals.update({'price_discount':  -1 * (partner_type.discount / 100)})
        #vals.update({'price_surcharge': partner_type_product.amount})
        res = product_pricelist_item_obj.create(vals)
        partner_type_product.product_pricelist_item_id = res.id

    partner_type_id = fields.Many2one('res.partner.type', 'Partner Type', ondelete='cascade')
    name = fields.Char('Name', readonly=True)
    type = fields.Selection([('product', 'By Product'),('category', 'By Category'),('merk', 'By Merk')], 'Type', required=True)
    product_id = fields.Many2one('product.template','Products')
    product_category_id = fields.Many2one('product.category', 'Product Category')
    product_merk_id = fields.Many2one('product.merk', 'Product Merk')
    product_pricelist_item_id = fields.Many2one('product.pricelist.item','Product Pricelist Item', reaodnly=True)

    @api.model
    def create(self, vals):
        name = ''
        if vals.get('type') == 'product':
            name += 'By Product : ' + self._get_product(vals.get('product_id')).name
        if vals.get('type') == 'category':
            name += 'By Category : ' + self._get_product_category(vals.get('product_category_id')).name
        if vals.get('type') == 'merk':
            name += 'By Merk : ' + self._get_product_merk(vals.get('product_merk_id')).name
        vals.update({'name': name})
        res = super(ResPartnerTypeProduct, self).create(vals)
        self._add_product_version(res)
        return res

    @api.multi
    def unlink(self):
        self.product_pricelist_item_id.unlink()
        return super(ResPartnerTypeProduct, self).unlink()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('partner_type_id')
    def onchange_partner_type_id(self):
        self.property_product_pricelist = self.partner_type_id.pricelist_id.id

    partner_type_id = fields.Many2one('res.partner.type', 'Partner Type')
    payment_method = fields.Selection([('cash','Cash'),('credit','Credit')],'Payment Method', default='Cash')
    payment_method_id = fields.Many2one('res.partner.payment.method', 'Payment Method')


class ResPartner(models.Model):
    _name = 'res.partner.payment.method'

    name = fields.Char('Name', size=50 , required=True)