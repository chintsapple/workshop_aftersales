from odoo import models, fields, api

from odoo.exceptions import ValidationError

# TODO: 6.1. Inherit an existing model to add new fields. Add at least 5 fields one of them must
#            be a relational field(O2M/M2M) and one notes field.


class Team(models.Model):

    _inherit = ['team.team', 'team.skill']
    _name = 'team.team'

    work_loc = fields.Selection(selection_add=[('rajkot', 'Rajkot'),
                                               ('mumbai', 'Mumbai')])
    # With selection_add attribute we can extend our selection fields

    workshop_loc_ids = fields.One2many('team.skill', 'location_id', 'Workshop Location')
    mobile = fields.Char('Mobile Number')
    note = fields.Text('Notes')
    # email = fields.Char('Email address', tracking=True)

    # to remove error of same column name and table name
    skill_ids = fields.Many2many('team.skill', 'team_new_skl_rel', 'team_id', 'skill_id', 'Skills')

    # TODO 6.4. Add an additional attribute in the existing field in inherited model. NOTE: This
    #           needs to be done in py.
    phone = fields.Char('Phone', readonly=True)

    # TODO 6.5. Modify an existing onchange method to be also called from an additional field and
    #           use this field in the logic to change other field’s value. It must call both the
    #           inherited method and also the existing method of the model.

    @api.onchange('gender', 'age')
    def onchnage_gender(self):
        print("Inherited Method gets called")
        for emp in self:
            if emp.age <= 18:
                emp.mobile = ''
            elif emp.age > 18:
                emp.mobile = '+918877889911'
        super(Team, self).onchnage_gender()
        print("Super Method gets called.")

    # TODO 6.6. Modify an existing constraint method to be also called from an additional field
    #           with an additional logic. Make sure the method in the existing method is not
    #           called and only overriden method is called.

    @api.constrains('emp_id', 'emp_code')
    def len_emp_id(self):
        for emp in self:
            print('emp.emp_code:', type(emp.emp_code))
            if not emp.emp_id and not emp.emp_code:
                raise ValidationError('Employee ID OR Employee Code is missing.')
            elif len(emp.emp_id) > 5:
                raise ValidationError('Employee ID could not be more than 4 Character!')
            elif int(len(emp.emp_code)) > 10:
                raise ValidationError('Employee Code should not be more than 10 Char.')

    # TODO 6.7. Modify an existing button’s method and call the existing method along with the
    #           button’s method.

    def add_skill(self):
        """
        Calling existing add_Skill button method as well as overriding it.
        """
        super(Team, self).add_skill()
        skill_obj = self.env['team.skill']
        skill_obj.create([{'name': 'ATF Service'}])

    # TODO 6.8. Add a new state in the existing list of states. Add a new button in the existing view
    #           to change the state to this state. Make sure the remaining flow is also followed.

    state = fields.Selection(selection_add=[('promoted', 'Promoted'), ('left',)])

    def emp_promotion(self):
        """
        This method will change state of candidates application to Left.
        @:param self: object pointer
        """
        for emp in self:
            emp.state = 'promoted'

    # TODO ERROR 6.9. Add a discount field on the Sale Order Line’s Tree view and form view of Odoo’s
    #                 sale module. Create a separate module for this called sale_discount_amount.

    # TODO ERROR 6.10. Add an Aadhar No field on Employee’s Form view and Tree view from hr module
    #                  of Odoo. Create a separate module for this hr_emp_aadhar.

    # TODO 6.11. Create a new model by inheriting two existing models. Add new fields in the
    #            inherited model. Create views where fields from all the 3 models should be there.
    #            Use _inherit.
    #      6.12. Add the Chatter functionality in your existing module. Add features like
    #            messaging, log, activity, followers and attachments.


class Team1(models.Model):

    _inherit = ['team.team', 'team.department']
    _name = 'team.teams'
    # _auto = False

    grade_10th = fields.Float('Grades In 10th')
    garde_12th = fields.Float('Grades in 12th')
    cgpa = fields.Float('CGPA')
    skill_ids = fields.Many2many('team.skill', 'teams_new_skl_rel', 'team_id', 'skill_id', 'Skills')

# TODO 6.21. Create a Template model. Use Delegate inheritance using this template model and
#            create a new model. Use the template model’s field in the new model’s view.


class Template(models.Model):

    _name = 'car.model'
    _rec_name = 'car_make'
    _description = 'Different Car different models'

    car_make = fields.Char('Car Make')

