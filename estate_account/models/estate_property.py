from odoo import models, Command

class estate_property(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        res =  super(estate_property,self).sold_action()

        move_type = "out_invoice"
        invoice_vals = {
            'partner_id': self.buyer_id,
            'move_type': move_type,
            'journal_id': self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal().id,
            'invoice_line_ids': [
                Command.create({ 'name': self.name, 'quantity': 1, 'price_unit': self.selling_price }),
                Command.create({ 'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100.00 }),
                Command.create({ 'name': 'Taxes', 'quantity': 1, 'price_unit': ((self.selling_price * 6)/100) })
            ]
        }

        self.env['account.move'].create(invoice_vals)
        return res