from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)



class FraudNumberRange(models.Model):
    _name = 'fraud.number.range'
    _description = 'Suspected Number Ranges'
    _rec_name = 'range_fraud'

    range_fraud = fields.Char(string="MSISDN_Range/IMSI/IMEI")
    # range_type = fields.Selection([
    #     ('msisdn', 'MSISDN'),
    #     ('imsi', 'IMSI'),
    #     ('imei', 'IMEI')
    # ], string='Range Type', required=True)

    range_type_id = fields.Many2one('range.type', string='Range Type', required=True)

    time_stamp = fields.Datetime(string='Time Stamp', default = fields.Datetime.now)
    description = fields.Text(string='Description')
    type_fraud = fields.Many2one('fraud.type',string='Fraud Type')
    status = fields.Selection([
        ('suspected', 'Suspected'),
        ('sent', 'Reported'),
        ('blocked', 'Blocked')
    ], string='Status', default='suspected')

    activity_ids = fields.One2many('fraud.number.range.line','fraud_id')


    detected_by = fields.Many2one('res.partner',string='Detected By')
    # detected_by = fields.Many2one('res.partner', string='Blocked By')
    detected_at = fields.Datetime(string="Detected at")

    reported_by = fields.Many2one('res.partner', string='Reported By')
    # reported_by = fields.Many2one('res.partner', string='Blocked By')
    reported_at = fields.Datetime(string="Reported at")

    # blocked_by = fields.Char(string='Blocked By')
    blocked_by = fields.Many2one('res.partner',string='Blocked By')
    blocked_at = fields.Datetime(string="Blocked at")


    def make_reported(self):
        self.status='sent'
        self.env['fraud.number.range.line'].create({
            'fraud_id':self.id,
            'status':'sent'
        })

    def make_blocked(self):
        self.status='blocked'
        self.env['fraud.number.range.line'].create({
            'fraud_id':self.id,
            'status':'blocked'
        })


class FraudNumberRangeLine(models.Model):
    _name = 'fraud.number.range.line'

    fraud_id = fields.Many2one('fraud.number.range')
    time_stamp = fields.Datetime(string='Time Stamp', default = fields.Datetime.now)
    status = fields.Selection([
        ('suspected', 'Suspected'),
        ('sent', 'Reported'),
        ('blocked', 'Blocked')
    ], string='Status', default='suspected')

class FraudType(models.Model):
    _name = 'fraud.type'

    name = fields.Char()

class RangeType(models.Model):
    _name = 'range.type'

    name = fields.Char()