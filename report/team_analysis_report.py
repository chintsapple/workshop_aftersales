from odoo import models, fields, api, tools

# TODO: 8.1. Create an Analysis report with numeric values in your module. Create a pivot
#            view with multiple rows, columns and measures.


class TeamAnalysis(models.Model):

    _name = 'team.analysis'
    _description = 'Team Analysis Report'

    _auto = False

    # employee_id = fields.Many2one('team.team', 'Employee')
    name = fields.Char('First Name', required=True)
    department_id = fields.Many2one('team.department', 'Department', ondelete='restrict')
    age = fields.Integer('age', default=21)
    exp = fields.Integer('Experience', help='Type experience in Years')
    create_uid = fields.Integer('UID')
    month = fields.Selection([(str(ele), str(ele)) for ele in range(1, 13)], 'Month')
    basic = fields.Float('Basic', tracking=True)
    total_gross_sal = fields.Float('Total Gross', compute='_calc_total_sal', store=True)
    total_net_sal = fields.Float('Total Net', compute='_calc_total_sal', store=True)
    allowance = fields.Float('Allowance')
    deduction = fields.Float('Deduction', tracking=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)

        self.env.cr.execute('''
                            CREATE OR REPLACE VIEW team_analysis AS(
                            SELECT ts.id, t.name, t.department_id, t.age, t.exp, ts.month, ts.basic,
                                    t.total_gross_sal, t.total_net_sal, ts.create_uid,
                                    ts.allowance, ts.deduction
                            FROM team t, team_salary ts
                            WHERE ts.employee_id = t.id
                            )
                            ''')

# CREATE OR REPLACE VIEW team_analysis AS(
#                             SELECT ts.id, ts.employee_id, t.department_id, t.age, t.exp, ts.month, ts.basic,
#                                     t.total_gross_sal, t.total_net_sal, ts.create_uid,
#                                     ts.allowance, ts.deduction
#                             FROM team t, team_salary ts
#                             WHERE ts.employee_id = t.id
