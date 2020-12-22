from odoo import models, fields, api


class Team(models.Model):

    _name = 'team.team'
    _description = 'Team'
    _auto = True  # this by default true, here I have mentioned for understanding only, it creates table automatically
    _table = 'team'  # This is given so we explicitly give table a name else table name will be team_team
    _order = 'name'  # used to show records in ascending order.

    # Personal info:
    name = fields.Char('First Name', required=True)
    ls_name = fields.Char('Last Name', required=True)
    res_address = fields.Text('Residential Address', required=True)
    per_address = fields.Text('Permanent Address')
    pin_code = fields.Char('Pin Code', size=6)
    # birthdate = fields.Date('Birthday', required=True)
    birthdate = fields.Date('Birthday', default=fields.datetime(1980, 1, 1))
    marital_status = fields.Selection([('single', 'Single'),
                                       ('Married', 'Married'),
                                       ('separated', 'Separated')], 'Marital Status')
    age = fields.Integer('age', default=21)
    blood = fields.Selection([('ab+', 'AB+'), ('ab-', 'AB-'),
                              ('b+', 'B+'), ('b-', 'B-'),
                              ('a+', 'A+'), ('a-', 'A-'),
                              ('o+', 'O+'), ('o-', 'O-')], 'Blood Group', required=True)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'female')], 'Gender')
    high_edu = fields.Selection([('graduate', 'Graduate'),
                                 ('under graduate', 'Under Graduate'),
                                 ('diploma', 'Diploma'),
                                 ('high school', 'High School'),
                                 ('iti', 'ITI')], 'Highest Education')
    msg = fields.Text('Message')
    template = fields.Html('Template')

    # Job Info
    title = fields.Char('Title')
    emp_id = fields.Char('Employee ID', size=4)
    department_id = fields.Many2one('team.department', 'Department', ondelete='restrict')
    work_loc = fields.Selection([('ahmedabad', 'Ahmedabad'),
                                 ('baroda', 'Baroda'),
                                 ('anand', 'Anand'),
                                 ('surat', 'Surat')], 'Work Location')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    salary_ids = fields.One2many('team.salary', 'employee_id', 'Salaries')
    skill_ids = fields.Many2many('team.skill', 'team_skl_rel', 'team_id', 'skill_id', 'Skills')

    # Emergency contact info
    full_name = fields.Char('Full Name', required=True)
    relationship = fields.Char('Relationship')
    skills = fields.Selection([('0', 'Trainee'),
                               ('1', 'Intern'),
                               ('2', 'Novice'),
                               ('3', 'Proficient'),
                               ('4', 'Expert')], 'Automobile Skill')
    contact = fields.Char('Contact Number')


class Department(models.Model):

    _name = 'team.department'
    _description = 'Department'

    _rec_name = 'dep_name'

    dep_name = fields.Char('Department Name')
    dep_code = fields.Char('Code', size=4)


class Salary(models.Model):

    _name = 'team.salary'
    _description = 'Salary'

    month = fields.Selection([(str(ele), str(ele)) for ele in range(1, 13)], 'Month')
    basic = fields.Float('Basic')
    allowance = fields.Float('Allowance')
    deduction = fields.Float('Deduction')
    employee_id = fields.Many2one('team.team', 'Employee')


class Skill(models.Model):

    _name = 'team.skill'
    _description = 'Skill'

    name = fields.Char('Name')

