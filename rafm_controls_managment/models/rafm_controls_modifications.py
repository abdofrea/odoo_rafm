# -*- coding: utf-8 -*-
from odoo import tools, api, fields, models
from datetime import datetime, timedelta, date


class RAFMModification(models.Model):
    _name = 'rafm.controls.modification'
    _description = 'RAFM Modification'

    name = fields.Char(string='Log', compute='_compute_name')
    time_stamp = fields.Datetime(string='TimeStamp', default=fields.Datetime.now)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User')
    control_id = fields.Many2one('rafm.control', string='Control')

    def _compute_name(self):
        for elem in self:
            elem.name = ''
            if elem.control_id and elem.time_stamp:
                elem.name = str(elem.control_id.rafm_id)+'_'+str(elem.time_stamp.strftime('%Y%m%d%H%M%S'))


