from odoo import fields, models
# TODO: 7.5. Create two wizards where first wizard will be called from menu and the second
#            wizard will be called from the button of the first wizard.


class UpdateExp(models.TransientModel):

    _name = 'update.exp'
    _description = 'Update the experience of employee'

    exp = fields.Integer('Experience', help='Type experience in Years')
    high_edu = fields.Selection([('graduate', 'Graduate'),
                                 ('under graduate', 'Under Graduate'),
                                 ('diploma', 'Diploma'),
                                 ('high school', 'High School'),
                                 ('iti', 'ITI')], 'Highest Education')
    name_id = fields.Many2one('team.team')

    def update_exp(self):
        """
        This method is used to update fields.
        """

        team = self.name_id
        team.write({'exp': self.exp})

    def update_edu(self):
        """
        This method is used to update fields.
        """

        team = self.name_id
        team.write({'high_edu': self.high_edu,
                    'exp': self.exp})
