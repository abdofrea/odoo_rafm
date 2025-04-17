from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class RALeakCase(models.Model):
    _name = 'ra.leak.case'
    _description = 'Revenue Assurance Leak Case'
    _order = 'date_reported desc'

    name = fields.Char(string='Case Title', required=True)
    
    category_id = fields.Many2one('ra.leak.category', string='Leak Category', required=True)
        
      
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity', default='medium')
    detection_method = fields.Char(string='Detection Method')
    date_reported = fields.Date(string='Date Reported', default=fields.Date.today)
    date_resolved = fields.Date(string='Date Resolved')
    detected_by_id = fields.Many2one('res.users',string='Detected By')
    
    impacted_revenue = fields.Float(string='Impacted Revenue (LYD)')
    saved_revenue = fields.Float(string='Saved Revenue (LYD)')

    description = fields.Text(string='Description')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ], string='Status', default='open')



class RALeakCaseType(models.Model):
    _name = 'ra.leak.category'

    name = fields.Char()

    #   [
    #     ('usage', 'Usage Leakage'),
    #     ('billing', 'Billing Error'),
    #     ('rating', 'Rating Issue'),
    #     ('reconciliation', 'Reconciliation Gap'),
    #     ('fraud', 'Fraud Related'),
    #     ('other', 'Other')
    # ])