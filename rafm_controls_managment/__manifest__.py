# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'RAFM Controls & Alarms Managment',
    'category': 'Extra',
    'summary': 'RAFM Daily Controls & Alarms Managment',
    'sequence': 10,
    'version': '1.0',
    'description': """RAFM Daily Controls & Alarms Managment""",
    'depends': ['base','project','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/rafm_control_view.xml',
        'views/rafm_data_source_view.xml',
        'views/rafm_frontend_view.xml',
        'views/rafm_cycle_view.xml',
        'views/rafm_category_view.xml',
        'views/rafm_modification_logs.xml',
        'views/rafm_controls_status.xml',
        'views/fraud_range_view.xml',
        'views/menuitems.xml',
        'wizard/register_modification_log_view.xml',
        'wizard/rafm_controls_status_log_view .xml',
        'data/daily_emails.xml'
    ],

    'images': ['static/description/icon.png'],
    
    'installable': True,
    'application': True,
}