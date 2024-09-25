from odoo import models, fields, api
import subprocess

class SysAdminWizard(models.TransientModel):
    _name = 'wizard'
    _description = 'Wizard'

    command_input = fields.Text(string="Command", required=True)
    output = fields.Text(string="Output", readonly=True)
    status_code = fields.Integer(string="Status Code", readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super(SysAdminWizard, self).default_get(fields_list)
        res.update({'output': '', 'status_code': 0})
        return res

    def execute_command(self):
        try:
            result = subprocess.run(
                self.command_input, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True
            )
            self.output = result.stdout
            self.status_code = result.returncode
        except Exception as e:
            self.output = str(e)
            self.status_code = -1

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
