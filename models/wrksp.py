from odoo import models, fields, api


class Team(models.Model):
    _name = 'team.team'
    _description = 'Team'
    _auto = True  # this by default true, here I have mentioned for understanding only, it creates table automatically
    _table = 'team'  # This is given so we explicitly give table a name else table name will be team_team
    _order = 'sequence'  # used to show records in ascending order.
    _parent_name = 'parent_id'  # Used to have parent child hierarchy to itself
    _parent_store = True  # by default it is `False`
    # Used to store the hierarchy int he parent path field
    # This makes it faster to search in the hierarchy, when true we all need to give path
    # Default value is given but if you change the field name,
    # you have to give that field as your _parent_name

    # Personal info:
    name = fields.Char('First Name', required=True)
    ls_name = fields.Char('Last Name', required=True)
    res_address = fields.Text('Residential Address', required=True)
    per_address = fields.Text('Permanent Address')
    pin_code = fields.Char('Pin Code', size=6)
    # birthdate = fields.Date('Birthday', required=True)
    birthdate = fields.Date('Birthday', default=fields.datetime(1980, 1, 1))
    marital_status = fields.Selection([('single', 'Single'),
                                       ('married', 'Married'),
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
    active = fields.Boolean('Active', default=True)
    photo = fields.Image('Photo')

    # Job Info
    comp_name = fields.Char('Company Name')
    exp = fields.Integer('Experience', help='Type experience in Years')
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
    total_gross_sal = fields.Float('Total Gross', compute='_calc_total_sal')
    # compute fields are not stored in database, with this attr `store=True` you can stored
    total_net_sal = fields.Float('Total Net', compute='_calc_total_sal')
    percent = fields.Float('Percentage', compute='_calc_total_sal')

    @api.depends('salary_ids')
    def _calc_total_sal(self):
        """
        Calculate total gross, total net and based on that
        calculate percentage salary.
        @:param self: object pointer and record set
        """

        for emp in self:
            total_gross_sal = 0.0
            total_net_sal = 0.0
            for sal in emp.salary_ids:
                total_gross_sal += sal.gross_sal
                total_net_sal += sal.net_sal

            emp.total_gross_sal = total_gross_sal
            emp.total_net_sal = total_net_sal
            emp.percent = total_gross_sal and (total_net_sal * 100 / total_gross_sal) or 0.0

    skill_ids = fields.Many2many('team.skill', 'team_skl_rel', 'team_id', 'skill_id', 'Skills')
    # resume = fields.Binary('Resume' attachment='False')  # If you want to store binary data into db.

    resume = fields.Binary('Resume')
    # resume = fields.Binary('Resume', attachment=False)  # by default attachment=True, that means whatever you
    # upload in this field will be not stored in database, because it's binary field you only get 1(s) n 0(s)
    # but if you want to stored in database you need to change attachment field to False and will be stored.
    add_cover_letter = fields.Boolean('Cover Letter')
    cover_let = fields.Text('Cover Letter')
    file_name = fields.Char('File Name')
    state = fields.Selection([('applied', 'Applied'),
                              ('interviewed', 'Interviewed'),
                              ('selected', 'Selected'),
                              ('rejected', 'Rejected'),
                              ('joined', 'Joined'),
                              ('left', 'Left')], 'State', default='applied')
    sequence = fields.Integer('Sequence')
    parent_id = fields.Many2one('team.team', 'Manager')
    parent_path = fields.Char('Parent Path', index=True)

    # Emergency contact info
    full_name = fields.Char('Full Name', required=True)
    relationship = fields.Char('Relationship')
    skills = fields.Selection([('0', 'Trainee'),
                               ('1', 'Intern'),
                               ('2', 'Novice'),
                               ('3', 'Proficient'),
                               ('4', 'Expert')], 'Automobile Skill')
    contact = fields.Char('Contact Number')
    reference = fields.Reference([('team.team', 'Team'),
                                  ('team.department', 'Department')], 'Reference')
    currency_id = fields.Many2one('res.currency', 'Currency')
    last_sal = fields.Monetary(currency_field='currency_id', string='Last Salary')

    # TODO 11.Print the current language of the system.
    #      12.Print the name of the current company.
    #      13.Print the name of the Current User
    #      14.Get the context from Environment
    #      15.Get the recordset of the form view which you have created for your model.
    #      16.Get the value of all predefined fields for a recordset containing one or more records.
    #      17. Filter the existing recordset with a condition. The condition should contain a field and a value.
    #      `18. Didn't understand`
    #      19. From a recordset get two fields character and integer such that the result would contain a
    #          single value which will be a concatenation of two fields mentioned above. For e.g. If you’re
    #          taking name and age it should be ‘Amar-25’.
    #      20. From a recordset get a list of values in a specific field.
    #      21. Sort a recordset in a descending order with a field. The action should be performed on a recordset only.
    #      22. Get three different recordset where first one will have all the records of a model,
    #          the second one will have few records of the model and third one will also have
    #          few records of that model. The condition of the later two recordset should not be
    #          same. Now check whether the later recordset are subset or superset of each other
    #          or not. Also check whether the first recordset is a superset or subset or not.
    #      23. Get the union, intersection and difference of two recordsets.

    def print_detail(self):
        """
        On click it will print language, current company, current user, context from environment,
        recordset of the model.
        """
        print("*" * 100)
        print("11. Current Language of the System: ", self.env.lang)
        print("12. Current Company: ", self.env.company)
        print("12.1 Current Company Name: ", self.env.company.name)
        print("13. Current User:", self.env.user)
        print("14. Context: ", self.env.context)
        print("15. Recordset: ", self)
        # print("16. Value of all predefined fields: ", list(self.env.values()))

        all_team = self.search([])
        print('all_team', all_team)
        positive_blood = all_team.filtered(lambda r: r.blood in ('ab+', 'a+', 'b+', 'o+'))
        print("17. Employee with Positive Blood Group:", positive_blood)
        # for p_blood in positive_blood:
        #     print(p_blood.name)
        exp_emp = all_team.mapped(lambda c: c.comp_name + '-' + str(c.exp))
        print("19. ==>")
        for emp in exp_emp:
            print("\t", emp)

        print('20. List of values of Title field:', all_team.mapped('title'))
        print('21. Recordset in descending order of Title field:', all_team.sorted('title', reverse=True))
        # TODO: TypeError: '<' not supported between instances of 'str' and 'bool'
        #                   Got this error comes due to I have not assigned `Title` field to all employee.
        #                   So when I tried to get `all_team.mapped('title')` it gives output like this:
        #       20. List of values of Title field: ['Maintenance Technician', 'System Technician (Drive Train)',
        #          'ITI', 'Human Resource', 'ITI', 'Diagnose Technician', 'System Technician',
        #          'Maintenance Technician', 'ITI', 'Vice President Landmark', False, False, False, False, False,
        #          False, False, False, False, False], this all False is boolean field because I haven't give any
        #          values in it so boolean values can't be sorted and other fields is a string where as False is
        #          boolean so sorted operation can't be performed, by giving values in `Title` field it will work.

        all_tech = self.search([])
        graduate_tech = self.search([('high_edu', '=', 'graduate')])
        iti_tech = self.search([('high_edu', '=', 'iti')])

        # checking subset `<`
        print("22. ==>")
        print("\t graduate_tech is subset of all_tech: ", graduate_tech < all_tech)
        print("\t graduate_tech is subset of iti_tech: ", graduate_tech < iti_tech)
        print("\t iti_tech is subset of all_tech: ", iti_tech < all_tech)
        print("\t iti_tech is subset of graduate_tech: ", iti_tech < graduate_tech)
        print("\t all_tech is subset of graduate_tech:", all_tech < graduate_tech)
        print("\t all_tech is subset of iti_tech:", all_tech < iti_tech)

        # Checking superset `>`
        print("\t graduate_tech is superset of all_tech: ", graduate_tech > all_tech)
        print("\t graduate_tech is superset of iti_tech: ", graduate_tech > iti_tech)
        print("\t iti_tech is superset of all_tech: ", iti_tech > all_tech)
        print("\t iti_tech is superset of graduate_tech: ", iti_tech > graduate_tech)
        print("\t all_tech is superset of graduate_tech:", all_tech > graduate_tech)
        print("\t all_tech is superset of iti_tech:", all_tech > iti_tech)

        # Union, Intersection and difference
        print("23. ==>")
        print("\t All Technician: ", all_tech)
        print("\t Graduate Technician: ", graduate_tech)
        print("\t ITI Technician: ", iti_tech)

        print("\t UNION of ITI Technician and Graduate Technician: ", iti_tech | graduate_tech)
        print("\t INTERSECTION of All Technician and Graduate Technician: ", all_tech & graduate_tech)
        print("\t DIFFERENCE of All Technician and ITI Technician: ", all_tech - iti_tech)
        print("*" * 100)

    # TODO: 24. Add a button on the form view when you click on this button it will create a
    #           record on a new model which does not have a relation with the current model.

    def add_skill(self):
        """
        Create new record for Skill Model
        """
        skill_obj = self.env['team.skill']
        skill_obj.create([{'name': 'Wiring Repair'},
                          {'name': 'Measurements'},
                          {'name': 'Break Bleeding'}])

    def add_team(self):
        """
        Create new record for Skill Model
        """
        emp_val_list = [{
            'name': 'Radhika',
            'ls_name': 'Dube',
            'age': 28,
            'gender': 'female',
            'res_address': 'Pune',
            'blood': 'ab+',
            'salary_ids': [(0, 0, {  # One2many fields
                'month': '2',
                'basic': 35000,
                'deduction': 3500,
                'allowance': 2000
            }), (0, 0, {
                'deduction': 4000,
                'month': '3',
                'allowance': 5000,
                'basic': 35000
            })],
            'skill_ids': [(4, 1), (4, 3), (4, 4)],  # Many2many fields
            'full_name': 'Usha Dube',

        }, {
            'name': 'Harshil',
            'ls_name': 'Patel',
            'age': 27,
            'gender': 'male',
            'res_address': 'Ahmedabad',
            'department_id': 4,
            'blood': 'b+',
            'salary_ids': [(0, 0, {  # One2many fields
                'month': '2',
                'basic': 35000,
                'deduction': 3500,
                'allowance': 2000
            }), (0, 0, {
                'deduction': 4000,
                'month': '3',
                'allowance': 5000,
                'basic': 35000
            })],
            'skill_ids': [(6, 0, [1, 5, 10])],
            'full_name': 'Nimisha Patel'
        }]
        self.create(emp_val_list)

    # TODO: 25. Add a button on the form view on the page of a one2many field. When you click
    #           this button it will add a record in the one2many field.

    def add_sal(self):
        """
        Create/write record for One2many field Salary.
        """
        salaries = {
            'salary_ids': [(0, 0, {
                'month': '2',
                'basic': 35000,
                'allowance': 2000,
                'deduction': 1500,
            }), (0, 0, {
                'month': '3',
                'basic': 30000,
                'allowance': 1500,
                'deduction': 1200
            })]
        }

        self.write(salaries)

    # TODO: 27. Add another button on the page of one2many field when you click on this button
    #           it will remove one record but it will not remove it from the database.

    def del_sal(self):
        """
        Delete existing record but not from the database.
        """
        delete_sal = {
            'salary_ids': [(3, 65), (3, 66)]
        }
        self.write(delete_sal)

    # TODO: 28. Add another button on the page of one2many field when you click on this button
    #           it will remove all the records in one2many.

    def del_all_sal(self):
        """
        Delete all existing record but not from the database.
        """
        delete_sal = {
            'salary_ids': [(5,)]
        }
        self.write(delete_sal)

    # TODO: 26. Add a button on the form view. When you click this button it should update a
    #           field’s value of the current record.

    def update_rec(self):
        """
        Update Existing record
        """
        em = {'email': 'abc@ymail.com'}
        self.write(em)

    # TODO: 29. Add a button on the form view when you click on it, it will link few existing
    #           records to the current model’s many2many field.

    def update_emp_skill(self):
        """
        Update skills of particular Employee
        """
        new_skill = {'skill_ids': [(4, 10), (4, 20)]}
        self.write(new_skill)

    # TODO: 30. Fetch 15 records from a model skipping first 5 records based on a condition and it
    #           should be sorted by name. `Here I give offset of 2 because recode does not have 15 ITI emp.

    def search_iti(self):
        """
        Search employees with ITI education
        """
        print("*" * 100)
        all_emps = self.search([])
        print("All Employees: ", all_emps)
        iti_emps = self.search([('high_edu', '=', 'iti')])
        print("All ITI employees: ", iti_emps)
        iti_emps = self.search([('high_edu', '=', 'iti')], limit=15, offset=2, order='name')
        print("Employees with ITI education order by name : ", iti_emps)
        print("*" * 100)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        print("DOM", domain)
        print("FIELDS", fields)
        print("GROUP BY", groupby)
        print("OFFSET", offset)
        print("LIMIT", limit)
        print("ORDER BY", orderby)
        print("LAZY", lazy)
        res = super(Team, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                           lazy=lazy)
        print("RESULT", res)
        return res

    # TODO: 31. Fetch the no of records based on a condition with and without using search method.

    def read_rec(self):
        """
        Read records of given fields
        """
        self.search([])
        emp_name_exp = self.read(['name', 'comp_name', 'exp'])  # load=''
        print(emp_name_exp)


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
    # employee_id = fields.Many2one('team.team', 'Employee', ondelete='cascade')
    gross_sal = fields.Float('Gross', compute='_calc_net_gross')
    net_sal = fields.Float('Net', compute='_calc_net_gross')

    @api.depends('basic', 'allowance', 'deduction')
    def _calc_net_gross(self):
        for sal in self:
            sal.gross_sal = sal.basic + sal.allowance
            sal.net_sal = sal.gross_sal - sal.deduction


class Skill(models.Model):
    _name = 'team.skill'
    _description = 'Skill'

    name = fields.Char('Name')

# TODO: Use domain in action from other model, like use to create action domain to show only `technicians`.
#       Hierarchy is not created.
