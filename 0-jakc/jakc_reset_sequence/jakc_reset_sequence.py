from openerp.osv import fields, osv

class reset_sequence(osv.osv):
    _name = 'reset.sequence'
    _description = "Reset Sequence"

    def sales_number_update(self, cr, uid, ids=None, context=None):
        sequence_obj = self.pool.get('ir.sequence')
        seq_id = sequence_obj.search(cr, uid, [('code', '=', 'sale.order')])
        if seq_id:
            sequence_obj.write(cr, uid, seq_id, {'number_next': 1})
        return None

    def purchase_number_update(self, cr, uid, ids=None, context=None):
        sequence_obj = self.pool.get('ir.sequence')
        seq_id = sequence_obj.search(cr, uid, [('code', '=', 'purchase.order')])
        if seq_id:
            sequence_obj.write(cr, uid, seq_id, {'number_next': 1})
        return None

