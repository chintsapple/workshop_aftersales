from odoo import models, fields, api


# TODO : 8.8. Create a wizard with multiple fields and create a wizard which will print
#             information from model for which the report is created and also from wizard’s
#             fields. Additionally use the parser to add atleast two methods.
#             NOTE : This must be a new wizard not the one mentioned in the exercise 4 same
#             goes for Parser file and report as well.


class QwebReportWizardMulti(models.TransientModel):

    _name = 'qweb.report.wizard.multi'
    _description = 'Additional fields to qweb report'

    date = fields.Date('Date', default=fields.Date.today())
    house_rent_allowance = fields.Integer('House Rent Allowance', default=15000.0)
    department_id = fields.Many2one('team.department', 'Department')
    employee_ids = fields.Many2many('team.team', string='Team')

    # TODO: Why it's not working without string `Team` attribute.

    @api.onchange('department_id')
    def onchange_dept(self):
        res = {}
        if self.department_id:
            self.employee_ids = [(5, 0, 0)]
            res['employee_ids'] = {
                'domain': [('department_id', '=', self.department_id.id)]
            }
        else:
            res['employee_ids'] = {
                'domain': []
            }
        return res

    def print_report(self):
        emp_obj = self.env['team.team']
        emps = self.employee_ids

        if not emps:
            if self.department_id:
                emp_dom = [('department_id', '=', self.department_id.id)]
            else:
                emp_dom = []
            emps = emp_obj.search(emp_dom)

        data = {
            'ids': emps.ids,
            'form': self.read()[0]
        }

        action_name = 'workshop_aftersales.action_team_report_wiz_pdf'
        report_action = self.env.ref(action_name).report_action(emps.ids, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action
