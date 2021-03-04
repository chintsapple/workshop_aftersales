from odoo import fields, models


class UpdateExp(models.TransientModel):

    _name = 'update.exp'
    _description = 'Update the experience of employee'

    exp = fields.Integer('Experience', help='Type experience in Years')

    def update_exp(self):
        """
        This method is used to update fields.
        """

        team = self.name_id
        print('team: ', team)

        if not team:
            print(self.exp)
            team_id = self.env.context.get('active_id')
            team = self.env['team.team'].browse(team_id)
            print('team updated: ', team)

        team.write({'exp': self.exp})
        print(self.exp)
