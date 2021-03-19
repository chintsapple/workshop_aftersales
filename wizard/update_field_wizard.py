from odoo import models, fields


class UpdateFields(models.TransientModel):

    _name = 'update.field'
    _description = 'Wizard to update some fields'

    # TODO 7.1. Create a wizard which will update a particular field of the selected record.
    name_id = fields.Many2one('team.team')
    salary_ids = fields.One2many('team.salary', 'employee_id', 'Salaries')
    pin_code = fields.Char('Pin Code', size=6)
    per_address = fields.Text('Permanent Address')

    def update_field(self):
        """
        This method is used to update fields.
        """

        team = self.name_id
        print('team: ', team)

        if not team:
            team_id = self.env.context.get('active_id')
            team = self.env['team.team'].browse(team_id)
            print('team updated: ', team)

        if self.pin_code:
            team.write({'pin_code': self.pin_code})

        # TODO 7.3. Call the same wizard to update the multiple records.
        if self.per_address:
            all_emp = self.env['team.team'].search([])
            # all_emp.write({'per_address': 'ahmedabad'})
            all_emp.write({'per_address': self.per_address})

# TODO: Doubt 7.6. Create a wizard where you will select a record of the model for which you have
#                  added a many2one field. The wizard’s button should display the records where the
#                  value selected in wizard is matching the many2one field’s value.
#             7.8. Open a tree view of the records from another record using object type button. Use
#                  Smart Button.
#             7.10. Inherit an existing wizard to add an additional field. Also use this field in the
#                  wizard’s method which is being called from the button.



