# -*- coding: utf-8 -*-
from odoo import tools, api, fields, models
import json
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.safe_eval import safe_eval

import logging

_logger = logging.getLogger(__name__)



class RAFMEmail(models.Model):
    _name = 'rafm.daily.email'
    _description = 'RAFM Email'

    all_controls = fields.Integer()
    all_covered_controls = fields.Integer()
    all_monetored_logs = fields.Integer()
    uncovered_controls = fields.Integer()
    status = fields.Text()  # Store JSON as string
    users = fields.Text()   # Store JSON as string
    domain = fields.Text()  # Store JSON as string


    def get_email_values(self):
        date_end = datetime.now().date() 
        date_start = date_end - timedelta(days=1)
        # date_start = datetime.now().date()
        # date_end = date_start + timedelta(days=1) 
        
        _logger.info(('date_start,date_end',date_start,date_end))
        big_dict = {}
        all_cpntrols_set = set([x.id for x in self.env['rafm.control'].search([])])
        covered_control_set = set()
        monitoring_logs = self.env['rafm.controls.status'].search([('time_stamp','>=',str(date_start)+' 00:00:00'),('time_stamp','<=',str(date_end)+' 00:00:00')])
        big_dict['all_controls'] = len(all_cpntrols_set)
        big_dict['all_covered_controls'] = set()
        big_dict['all_monetored_logs'] = len(monitoring_logs)
        big_dict['status']= {}
        big_dict['users']= {}
        big_dict['domain']= {}

        for elem in monitoring_logs:
            covered_control_set.add(elem.control_id.id)
            big_dict['status'].setdefault(elem.status,0)
            big_dict['status'][elem.status] += 1
            big_dict['all_covered_controls'].add(elem.control_id.id)
            big_dict['users'].setdefault(elem.user_id.name,{'logs':0, 'covered_controls':set()})
            big_dict['users'][elem.user_id.name]['logs'] += 1
            big_dict['users'][elem.user_id.name]['covered_controls'].add(elem.control_id.id)
            big_dict['domain'].setdefault(elem.control_id.domain,0)
            big_dict['domain'][elem.control_id.domain] += 1
        
        for user in big_dict['users'].keys():
            big_dict['users'][user]['covered_controls'] = len(big_dict['users'][user]['covered_controls'])

        big_dict['all_covered_controls'] = len(big_dict['all_covered_controls'])
        big_dict['uncovered_controls'] = len(all_cpntrols_set - covered_control_set)
        
        record_data = {
            'all_controls': big_dict['all_controls'],
            'all_covered_controls': big_dict['all_covered_controls'],
            'all_monetored_logs': big_dict['all_monetored_logs'],
            'status': json.dumps(big_dict['status']),
            'users': json.dumps(big_dict['users']),
            'domain': json.dumps(big_dict['domain']),
            'uncovered_controls': big_dict['uncovered_controls']
            }
        
        report_record = self.env['rafm.daily.email'].create(record_data)
        template = self.env.ref('rafm_controls_managment.email_template_daily_report')
        # rendered_body = template._render_template(template.body_html, 'rafm.daily.email', [report_record.id])[report_record.id]
        context = {
            'object': report_record,  # Make sure 'object' is this record
            'all_controls': report_record.all_controls,
            'all_covered_controls': big_dict['all_covered_controls'],
            'all_monetored_logs': report_record.all_monetored_logs,
            'status': json.loads(report_record.status or '{}'),
            'uncovered_controls': report_record.uncovered_controls,
            'users': json.loads(report_record.users or '{}'),
            'domain': json.loads(report_record.domain or '{}'),
        }
        # Send the email
        # _logger.info("big_dict",context)
        template.with_context(context).send_mail(report_record.id)