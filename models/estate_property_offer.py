# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', default=datetime.today() + timedelta(days=7))
    property_type_id = fields.Many2one("estate.property", string="Property Type")
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for lead in self:
            if lead.validity and lead.validity > 0:
                if lead.create_date:
                    lead.date_deadline = lead.create_date + timedelta(days=lead.validity)
                else:
                    lead.date_deadline = datetime.today() + timedelta(days=lead.validity)
                    
    @api.model
    def create(self, vals):
        if float_compare(vals['price'], max(self.env['estate.property.offer'].search([('property_id', '=', vals['property_id'])]).mapped('price'), default=0), precision_rounding=2) == -1:
            raise ValidationError('One offer with a lower amount than an existing offer can not be created.')
        self.env['estate.property'].browse(vals['property_id']).update({'status':'offer_received'})
        return super(PropertyOffer, self).create(vals)

    def _inverse_date_deadline(self):
        for lead in self:
            if lead.create_date and lead.date_deadline:
                lead.validity = (datetime(lead.date_deadline.year, lead.date_deadline.month, lead.date_deadline.day) - lead.create_date).days
            else:
                lead.validity = 0
    
    def action_accept(self):
        for record in self:
            if (self.search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])):
                raise UserError('Only one offer can be accepted.')
            if float_compare(record.price, 0.9 * record.property_id.expected_price, precision_rounding=2) == -1:
                raise ValidationError('The selling price must at least 90% of the expected price!. You must reduce the expected price if you want to accept this offer.')
        self.update({'status': 'accepted'})
        self.env['estate.property'].search([('id', '=', self.property_id.id)]).update({'selling_price': self.price, 'buyer_id': self.partner_id.id, 'status': 'offer_accepted'})
        return True

    def action_refuse(self):
        self.update({'status': 'refused'})
        return True
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The Offer Price must be strictly positive')
        ]