from odoo import models, fields



class RAFMControlCategory(models.Model):
    _name = 'rafm.control.category'
    _description = 'RAFM Control Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')

