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

    date_reported = fields.Date(string='Date Reported', default=fields.Date.today, required=True)

    date_started = fields.Datetime(string='Case started at', required=True)
    date_resolved = fields.Datetime(string='Date Resolved')

    case_duration = fields.Char(string="Total Case duration", compute="_get_case_duration")

    detected_by_id = fields.Many2one('res.users',string='Detected By' , required=True)
    
    impacted_revenue = fields.Float(string='Impacted Revenue (LYD)')

    total_loss_revenue = fields.Float(string='Impacted Revenue (LYD)', store=True, compute="get_impacted_revenue")

    saved_revenue = fields.Float(string='Saved Revenue (LYD)')

    description = fields.Text(string='Description')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ], string='Status', default='open')

    leak_line_ids = fields.One2many('ra.leak.case.line','leak_id')

    def close_case(self):
        if not self.date_resolved:
            raise ValidationError('Please enter Date Resolved!')
        self.status = 'closed'

    def inprogress_case(self):
        self.status = 'in_progress'

    def action_set_open(self):
        self.status = 'open'

    @api.onchange('date_started','date_resolved')
    def _get_case_duration(self):
        for elem in self:
            elem.case_duration = ''
            if elem.date_started and elem.date_resolved:
                elem.case_duration = str(elem.date_resolved - elem.date_started )

    @api.depends('leak_line_ids', 'impacted_revenue')
    def get_impacted_revenue(self):
        for rec in self:
            total = 0.0
            if rec.leak_line_ids:
                total = sum((l.total_loss or 0.0) for l in rec.leak_line_ids)
            total += (rec.impacted_revenue or 0.0)
            rec.total_loss_revenue = float(total)

    def copy(self, default=None):
        default = dict(default or {})
        # remove the unique field if not supplied by caller
        default.setdefault('status', 'open')
        default.setdefault('date_started', False)
        default.setdefault('date_reported', fields.Date.today())
        default.setdefault('date_resolved', False)
        default.setdefault('detection_method', False)
        default.setdefault('name', (self.name or '') + '-COPY')
        default.setdefault('leak_line_ids', False)
        default.setdefault('description', False)
        default.setdefault('impacted_revenue', False)
        return super().copy(default)

class RALeakCaseLine(models.Model):
    _name = 'ra.leak.case.line'

    leak_id = fields.Many2one('ra.leak.case')
    name = fields.Char(string='Description', required=True)
    unit = fields.Selection([
        ('mm', 'Duration/Minutes'),
        ('ss', 'SMS Count'),
        ('gg', 'Data Usage/Gbyte'),
        ('other', 'Other Metric (mention it in the description)')], string='Loss Unit / Count', required=True)
    unit_count = fields.Float(string='Unit Count', required=True)
    unit_cost = fields.Float(string='Unit Cost', required=True)
    total_loss  = fields.Float(string='Total Loss', compute="_get_total_loss")

    @api.onchange('unit_count','unit_cost')
    def _get_total_loss(self):
        for elem in self:
            elem.total_loss = elem.unit_count * elem.unit_cost



class RALeakCaseType(models.Model):
    _name = 'ra.leak.category'
    name = fields.Char()
