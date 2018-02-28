from openerp import models, fields, api
import base64
import csv
import cStringIO
from datetime import datetime
import logging
import zipfile

_logger = logging.getLogger(__name__)


AVAILABLE_PRODUCT_STATE = [
    ('draft','In Development'),
    ('sellable','Normal'),
    ('end','End of Lifecyle'),
    ('obsolete','Obsolete'),
    ('non_active','Non Active'),
]

class Product_merk(models.Model):
    _name = 'product.merk'

    name = fields.Char('Merk', size=50, required=True)


class Product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    merk_id = fields.Many2one('product.merk','Merk')
    warna = fields.Char('Color', size=50)
    motif = fields.Char('Motif', size=50)
    page = fields.Char('Page', size=100)
    state = fields.Selection(AVAILABLE_PRODUCT_STATE,'Status')


class ProductImageImport(models.Model):
    _name = 'product.image.import'

    @api.one
    def process_image_import(self):
        #Convert Base64 string to zipfile
        output_file = open('/tmp/product_image.zip', 'w')
        data = base64.b64decode(self.attachment)
        output_file.write(data)

        #Exctract Zipfile
        image_zip_file = zipfile.ZipFile('/tmp/product_image.zip', 'w')
        dirname = datetime.now().strftime('%Y%m%d%H%M%S')
        image_zip_file.extractall('/tmp/' + dirname)
        image_zip_file.close()

        #Looping to update Product Picture
        _logger.info('Procces Image Import')

    name = fields.Date('Date', default=datetime.now())
    attachment = fields.Binary('Zip File')
