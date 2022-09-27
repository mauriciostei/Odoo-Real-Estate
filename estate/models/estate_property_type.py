
from odoo import models, fields, api

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Real estate properties Types"
    _order = "sequence"

    name = fields.Char( required=True )
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property", "property_type_id", String="Properties")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_count_types")

    @api.depends("offer_ids")
    def _count_types(self):
        for record in self:
            record.offer_count = len(record.offer_ids)