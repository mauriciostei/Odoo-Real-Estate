
from email.policy import default
from odoo.exceptions import ValidationError
from odoo import models, fields, api, exceptions

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Real estate properties"
    _order = "id desc"

    name = fields.Char( required=True )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date( copy=False, default=lambda self: fields.Datetime.now() )
    expected_price = fields.Float( required=True )
    selling_price = fields.Float( readonly=True, copy=False )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection( selection = [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')] )
    state = fields.Selection( default='New', copy=False , selection = [('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')] )
    active = fields.Boolean( default=True )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_total_area")
    best_price = fields.Float(compute="_best_price")

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price >= 0)', 'A property expected price must be strictly positive'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'A property selling price must be positive')
    ]

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends("offer_ids.price")
    def _best_price(self):
        for line in self:
            if(len(line.offer_ids) > 0):
                line.best_price = max(line.offer_ids.mapped("price"))
            else:
                line.best_price = 0

    @api.onchange("garden")
    def _onchange_garder(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def sold_action(self):
        for record in self:
            if record.state == "Canceled":
                raise exceptions.UserError('Las propiedades canceladas no pueden ser vendidas')
            else:
                record.state = "Sold"
        return True

    def cancel_action(self):
        for record in self:
            if record.state == "Sold":
                raise exceptions.UserError('Las propiedades Vendidas no pueden ser canceladas')
            else:
                record.state = "Canceled"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if(record.selling_price > 0):
                percent = (record.expected_price * 90) / 100
                if(record.selling_price < percent):
                    raise ValidationError("El precio de venta no puede ser inferior en un 90% al precio esperado")
                    

    @api.ondelete(at_uninstall=False)
    def _unlink_by_state(self):
        for record in self:
            if record.state not in ('New', 'Canceled'):
                raise exceptions.UserError('No se puede borrar estas propiedades')