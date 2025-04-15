# -*- coding: utf-8 -*-
from odoo import tools, api, fields, models
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class RAFMStatus(models.Model):
    _name = 'rafm.controls.status'
    _description = 'RAFM Status'

    name = fields.Char(string='Log', compute='_compute_name')
    status = fields.Selection([
        ('pass', 'Pass'),
        ('etl_issue', 'ETL Issue'),
        ('suspected', 'Suspected')
    ], string='Control Status', required=True)
    time_stamp = fields.Datetime(string='TimeStamp', default=fields.Datetime.now)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User')
    control_id = fields.Many2one('rafm.control', string='Control')

    def _compute_name(self):
        for elem in self:
            elem.name = ''
            if elem.control_id and elem.time_stamp:
                elem.name = str(elem.control_id.rafm_id)+'_'+str(elem.time_stamp.strftime('%Y%m%d%H%M%S'))


# access_controls_status_wizard,access_controls_status_wizard,model_rafm_controls_status_wizard,,1,1,1,1
