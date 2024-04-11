# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    
    name = fields.Char(string="Property Type")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property", "property_type_id", string="Offers" )
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    
    @api.depends('offer_ids.property_type_id')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = record.offer_ids.search_count([('property_type_id','=',record.id)])
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'A property type name must be unique!')
    ]
    