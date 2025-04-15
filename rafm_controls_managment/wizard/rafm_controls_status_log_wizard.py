from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class RAFMControlStatusWizard(models.TransientModel):
    _name = 'rafm.controls.status.wizard'
    _description = 'RAFM Status Wizard'
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(RAFMControlStatusWizard, self).default_get(fields_list)
        context_control_id = self.env.context.get('control_id')
        context_status = self.env.context.get('status')
        defaults['control_id'] = context_control_id
        defaults['status'] = context_status

        return defaults

    text_input = fields.Char(string="Enter Description")  # Single text field
    time_stamp = fields.Datetime(string='TimeStamp', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    control_id = fields.Many2one('rafm.control', string='Control')
    status = fields.Selection([
        ('pass', 'Pass'),
        ('etl_issue', 'ETL Issue'),
        ('suspected', 'Suspected')
    ], string='Control Status')

    def confirm_action(self):
        vals={
            'description':self.text_input,
            'time_stamp':self.time_stamp,
            'user_id':self.user_id.id,
            'control_id':self.control_id.id,
            'status':self.status
        }
        # _logger.info(vals)
        self.env['rafm.controls.status'].create(vals)
