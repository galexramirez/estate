# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"
    
    name = fields.Char(string="Property Type")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'A property type name must be unique!')
    ]
    