from odoo import models, fields



class RAFMDataSource(models.Model):
    _name = 'rafm.data.source'
    _description = 'RAFM Data Source'

    name = fields.Char(string='Source Name', required=True)
    description = fields.Text(string='Description')

