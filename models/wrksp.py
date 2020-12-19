from odoo import models, fields, api


class Team(models.Model):

    _name = 'team.team'
    _description = 'Team'
    _auto = True  # this by default true, here I have mentioned for understanding only, it creates table automatically
    _table = 'team'  # This is given so we explicitly give table a name else table name will be team_team

    name = fields.Char('Name', required=True)
    birthdate = fields.Date('Birthday', required=True)
    age = fields.Integer('age')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'female')], 'Gender')
    high_edu = fields.Selection([('graduate', 'Graduate'),
                                 ('under graduate', 'Under Graduate'),
                                 ('diploma', 'Diploma'),
                                 ('high school', 'High School'),
                                 ('iti', 'ITI')], 'Highest Education')
    msg = fields.Text('Message')
    template = fields.Html('Template')



    # Integer
    # ◦ Float
    # ◦ Boolean
    # ◦ Char
    # ◦ Text
    # ◦ Html
    # ◦ Date
    # ◦ Datetime
    # ◦ Selection
