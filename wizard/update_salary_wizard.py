from odoo import models, fields

# TODO: 7.4. Create another wizard which will add records on the one2many field


class UpdateSalary(models.TransientModel):

    _name = 'update.salary'
    _description = 'Wizard to update salary of particular employee'

    month = fields.Selection([(str(ele), str(ele)) for ele in range(1, 13)], 'Month')
    basic = fields.Float('Basic', tracking=True)
    allowance = fields.Float('Allowance')
    deduction = fields.Float('Deduction', tracking=True)
    employee_id = fields.Many2one('team.team', 'Employee')
    # salary_ids = fields.One2many('team.salary', 'employee_id', 'Salaries')

    def update_salary(self):

        salary = self.employee_id
        print("context", self._context)
        # {'lang': 'en_US', 'tz': 'Asia/Calcutta', 'uid': 2, 'allowed_company_ids': [1]}

        salary.write({
            'salary_ids': [(0, 0, {
                'month': self.month,
                'basic': self.basic,
                'allowance': self.allowance,
                'deduction': self.deduction})]
        })
