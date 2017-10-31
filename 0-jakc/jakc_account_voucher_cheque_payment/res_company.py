from openerp.osv import fields, osv


class res_company(osv.osv):
    _inherit = 'res.company'

    _columns =  {
        'cheque_journal_id' : fields.many2one('account.journal','Check Journal'),
    }

