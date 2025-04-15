from odoo import models, fields


class RAFMFrontend(models.Model):
    _name = 'rafm.controls.frontend'
    _description = 'RAFM Frontend'

    name = fields.Char(string='Frontend Name', required=True)
    system_type = fields.Selection([
        ('web', 'Web'),
        ('mobile', 'Mobile'),
        ('desktop', 'Desktop')
    ], string='System Type')
