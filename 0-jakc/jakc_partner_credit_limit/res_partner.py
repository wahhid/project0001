#-*- coding:utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning



class ResPartner(models.Model):
    _inherit = 'res.partner'

    allow_credit = fields.Boolean('Allow Credit', default=False)
