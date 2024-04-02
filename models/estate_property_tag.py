# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    
    name = fields.Char(string="Name", required=True)