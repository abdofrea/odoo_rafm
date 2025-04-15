from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class RAFMControl(models.Model):
    _name = 'rafm.control'
    _description = 'RAFM Control'
    _rec_name='rafm_id'

    rafm_id = fields.Char(string='ID', required=True)
    audit_name = fields.Char(string='Audit Name', required=True)
    source_nodes = fields.Many2many('rafm.data.source', string='Source Nodes')
    domain = fields.Selection([
        ('ra', 'RA'),
        ('fm', 'FM'),
        ('rafm', 'RAFM')
    ], string='Domain', required=True)

    critical_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Critical Level', required=True)

    assigned_ids = fields.Many2many(
        'res.users',
        string='Responsible users',
        help='Select multiple users related to this record.'
    )

    reason = fields.Text(string='Reason')
    url = fields.Char(string="URL")

    category_id = fields.Many2one('rafm.control.category', string='Category', required=True)
    
    frontend_id = fields.Many2many('rafm.controls.frontend', string='Frontend')
    audits_generation_cycle_id = fields.Many2many('rafm.controls.cycle', string='Audits Generation Cycle')
    modifications_ids = fields.One2many('rafm.controls.modification','control_id',string='Modification Logs')

    checked_recently = fields.Boolean(compute="_compute_checked_recently", store=True)


    def _compute_checked_recently(self):
        # time for control to hide after check 
        hide_duration =2*60*60
        for elem in self:
            # _logger.info(('_compute_checked_recently',elem.rafm_id))
            elem.checked_recently = False
            query = "select max(time_stamp) from rafm_controls_status where control_id = %s and user_id = %s"
            self.env.cr.execute(query, (elem.id, self.env.user.id))
            result = self.env.cr.fetchone()
            # _logger.info(('result',result))
            if result[0]:
                delta = datetime.now() - result[0]
                if delta.total_seconds() < hide_duration:
                    elem.checked_recently = True

    @api.constrains('rafm_id')
    def _check_rafm_id_constraints(self):
        for record in self:
            if len(record.rafm_id) != 6:
                raise ValidationError("The ID must be in this format RF-XXX.")
            if self.search_count([('rafm_id', '=', record.rafm_id)]) > 1:
                raise ValidationError("The ID must be unique.")

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        super().search([])._compute_checked_recently()
        res = super().search(args, offset=offset, limit=limit, order=order, count=count)
        return res

    def open_modification_log_wizard(self):
        """Open the wizard when clicking the smart button"""
        vals = {
            'name': 'Modification Log',
            'type': 'ir.actions.act_window',
            'res_model': 'rafm.controls.modification.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('rafm_controls_managment.rafm_controls_modification_wizard').id,
            'target': 'new',
            'context': {'control_id': self.id},
        }
        return vals 
    
    def make_pass(self):
        ControlStatus = self.env['rafm.controls.status']
        current_user = self.env.user

        for record in self:
            ControlStatus.create({
                'user_id': current_user.id,
                'control_id': record.id,
                'status': 'pass',
            })
        self._compute_checked_recently()

    def make_etl_issue(self):
        vals = {
            'name': 'Control Status Log',
            'type': 'ir.actions.act_window',
            'res_model': 'rafm.controls.status.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('rafm_controls_managment.rafm_controls_status_wizard').id,
            'target': 'new',
            'context': {'control_id': self.id, 'status':'etl_issue'},
        }
        return vals 
    
    def make_suspected(self):
        vals = {
            'name': 'Control Status Log',
            'type': 'ir.actions.act_window',
            'res_model': 'rafm.controls.status.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('rafm_controls_managment.rafm_controls_status_wizard').id,
            'target': 'new',
            'context': {'control_id': self.id, 'status':'suspected'},
        }
        return vals 
    