from odoo import models, fields


class UpdateFields(models.TransientModel):

    _name = 'update.field'
    _description = 'Wizard to update some fields'

    # TODO 7.1. Create a wizard which will update a particular field of the selected record.
    name_id = fields.Many2one('team.team')
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

        team.write({'pin_code': self.pin_code})

        # TODO 7.3. Call the same wizard to update the multiple records.
        all_emp = self.env['team.team'].search([])
        # all_emp.write({'per_address': 'ahmedabad'})
        all_emp.write({'per_address': self.per_address})


