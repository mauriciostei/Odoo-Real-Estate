
from odoo import models, fields

class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate properties Tags"
    _order = "name"

    name = fields.Char( required=True )
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'A property tag name and property type name must be unique')
    ] 