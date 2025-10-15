from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class RAFMRiskSus(models.Model):
    _name = 'rafm.risk.suspect'
    _description = 'RAFM Risk under Monitoring'
    _order = 'date_reported desc'

    name = fields.Char(string='Case Title', required=True)

    category_id = fields.Many2one('ra.leak.category', string='Leak Category', required=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity', default='medium')
    status = fields.Selection([
        ('under_monitoring', 'Under Monitoring'),
        ('resolved', 'Resolved'),
        ('under_investigation', 'Under Investigation'),
    ], string='Status', default='under_monitoring')
    risk_type = fields.Selection([
        ('quantitative', 'Quantitative'),
        ('qualitative', 'Qualitative'),
    ], string='Risk type', required=True)
    observed_by_id = fields.Many2many('res.users', string='Observed By')
    saved_revenue = fields.Float(string='Estimated Average Annual Revenue Loss L.D')
    description = fields.Text(string='Description')