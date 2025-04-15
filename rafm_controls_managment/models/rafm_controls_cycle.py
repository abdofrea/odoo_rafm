from odoo import models, fields



class RAFMCycle(models.Model):
    _name = 'rafm.controls.cycle'
    _description = 'RAFM Audit Generation Cycle'

    name = fields.Char(string='Cycle Name', required=True)
    