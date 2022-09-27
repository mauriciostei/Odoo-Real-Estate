
from datetime import timedelta
import datetime
from odoo import models, fields, api, exceptions

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate properties offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection( copy=False, selection = [('Accepted', 'Accepted'), ('Refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True )
    property_id = fields.Many2one("estate.property", string="Property", required=True )
    validity = fields.Integer( default=7 )
    date_deadline = fields.Date( compute="_set_date", inverse="_set_validity")

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('price_positive', 'CHECK(price >= 0)', 'An offer price must be strictly positive')
    ]

    @api.depends("validity")
    def _set_date(self):
        for line in self:
            if not line.create_date:
                line.date_deadline = datetime.datetime.now() + timedelta(days=line.validity)
            else:
                line.date_deadline = line.create_date + timedelta(days=line.validity)

    def _set_validity(self):
        for line in self:
            d1 = line.create_date.date()
            d2 = line.date_deadline
            line.validity = abs((d2 - d1).days)

    def accept_action(self):
        for record in self:
            record.status = "Accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "Offer Accepted"
        return True

    def refuse_action(self):
        for record in self:
            record.status = "Refused"
        return True

    @api.model
    def create(self, vals):

        property = self.env['estate.property'].browse(vals['property_id'])
        property.state = "Offer Received"

        for offer in property.offer_ids:
            if offer.price > vals['price']:
                raise exceptions.UserError('No se puede generar la oferta, es meno a una previamente creada')

        return super().create(vals)