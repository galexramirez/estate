# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    
    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', default=datetime.today() + timedelta(days=7))
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for lead in self:
            if lead.validity and lead.validity > 0:
                if lead.create_date:
                    lead.date_deadline = lead.create_date + timedelta(days=lead.validity)
                else:
                    lead.date_deadline = datetime.today() + timedelta(days=lead.validity)

    def _inverse_date_deadline(self):
        for lead in self:
            if lead.create_date and lead.date_deadline:
                lead.validity = (datetime(lead.date_deadline.year, lead.date_deadline.month, lead.date_deadline.day) - lead.create_date).days
            else:
                lead.validity = 0
    
    def action_accept(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('Only one offer can be accepted.')
        self.update({'status': 'accepted'})
        return True

    def action_refuse(self):
        self.update({'status': 'refused'})
        return True
