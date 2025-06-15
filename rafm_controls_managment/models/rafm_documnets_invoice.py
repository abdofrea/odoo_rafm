from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)



class RafmInvoiceDocuments(models.Model):
    _name = 'rafm.invoice.document'
    _description = 'RAFM Invoices And Document'

    name = fields.Char(string="Title", required=True)

    document_type_id = fields.Many2one('rafm.invoice.document.type', string='Document Type')
    time_stamp = fields.Datetime(string='Time Stamp', default = fields.Datetime.now)
    description = fields.Text(string='Description')
    document_ids = fields.One2many('rafm.invoice.document.line','document_id')



class RafmInvoiceDocumnetsLine(models.Model):
    _name = 'rafm.invoice.document.line'

    document_id = fields.Many2one('rafm.invoice.document')
    time_stamp = fields.Datetime(string='Time Stamp', default = fields.Datetime.now)
    attachment_id = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string="File Name")


class RafmInvoiceDocumnetsType(models.Model):
    _name = 'rafm.invoice.document.type'
    name = fields.Char()

