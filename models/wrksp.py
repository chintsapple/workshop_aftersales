from odoo import models, fields, api

from odoo.exceptions import ValidationError


class Team(models.Model):
    _name = 'team.team'
    _description = 'Team'
    _auto = True  # this by default true, here I have mentioned for understanding only,
#                   it creates table automatically
    _table = 'team'  # This is given so we explicitly give table a name else table name will be team_team
    _order = 'sequence'  # used to show records in ascending order.
    _parent_name = 'parent_id'  # Used to have parent child hierarchy to itself
    _parent_store = True  # by default it is `False`
    # Used to store the hierarchy int he parent path field
    # This makes it faster to search in the hierarchy, when true we all need to give path
    # Default value is given but if you change the field name,
    # you have to give that field as your _parent_name

    # TODO 4.13. Add an SQL constraint to add a check constraint to check the value of a field.
    #      4.18. Add an SQL constraint to check a field’s value is not greater than a specific number.
    _sql_constraints = [
        ('check_age', 'check(age >= 18)', 'Child labor not allowed!'),
        ('check_exp', 'check(exp <= 10)', ' You have 10+ years of experience, now live life.'),
    ]

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
    emp_id = fields.Char('Employee ID')
    emp_code = fields.Char('Employee Code')
    department_id = fields.Many2one('team.department', 'Department', ondelete='restrict')
    work_loc = fields.Selection([('ahmedabad', 'Ahmedabad'),
                                 ('baroda', 'Baroda'),
                                 ('anand', 'Anand'),
                                 ('surat', 'Surat')], 'Work Location')
    phone = fields.Char('Phone')
    email = fields.Char('Email address')

    salary_ids = fields.One2many('team.salary', 'employee_id', 'Salaries')
    total_gross_sal = fields.Float('Total Gross', compute='_calc_total_sal', store=True)
    # compute fields are not stored in database, with this attr `store=True` you can stored
    total_net_sal = fields.Float('Total Net', compute='_calc_total_sal', store=True)
    percent = fields.Float('Percentage', compute='_calc_total_sal')

    # TODO: 4.14. Add an object constraint to make sure that the length of a character field is
    #             exactly 4 characters.
    @api.constrains('emp_id')
    def len_emp_id(self):
        for emp in self:
            if not emp.emp_id:
                raise ValidationError('Employee ID missing.')
            elif len(emp.emp_id) > 4:
                raise ValidationError('Employee ID could not be more than 4 Character!')

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
    colors = fields.Integer('Colors')
    join_date = fields.Date('Joined Date')
    training_start = fields.Datetime('Training Start Date')
    training_end = fields.Datetime('Training End Date')

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
    incentive = fields.Float('Incentive')

    # TODO 11. Print the current language of the system.
    #      12. Print the name of the current company.
    #      13. Print the name of the Current User
    #      14. Get the context from Environment
    #      15. Get the recordset of the form view which you have created for your model.
    #      `16. Get the value of all predefined fields for a recordset containing one or more records.`
    #      17. Filter the existing recordset with a condition. The condition should contain a field and a value.
    #      `18. Filter an existing record on a field such that if only the records which do not have
    #          a value in the field should be displayed.`
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

    # TODO: 4.4. Override default_get method to add default fields when the record is created.
    #       4.15. Create a Sequence for an object and fetch the sequence as default value to a field.
    # @api.model
    # def default_get(self, fields):
    #     seq_obj = self.env['ir.sequence']
    #     res = super(Team, self).default_get(fields)
    #     res['emp_code'] = seq_obj.next_by_code('team.team')
    #     res.update({'email': 'abc@gmail.com'})
    #     return res

    # # TODO: 4.16. Create a sequence and assign it on creation of the record.
    # @api.model_create_multi
    # def create(self, vals_lst):
    #     seq_obj = self.env['ir.sequence']
    #     for emp_vals in vals_lst:
    #         emp_vals['emp_code'] = seq_obj.next_by_code('team.team')
    #     return super(Team, self).create(vals_lst)

    # TODO:4.17. Create a sequence and assign it’s value on a button click.
    def add_seq(self):
        print("self=================:", self)
        seq_obj = self.env['ir.sequence']
        self.write({'emp_code': seq_obj.next_by_code('team.team')})
        # for i in self:
        #     i.write({'emp_code': seq_obj.next_by_code('team.team')})

    # TODO: 4.7. Add an onchange method for a field where it will update values of two other
    #            fields.
    @api.onchange('gender')
    def onchnage_gender(self):
        for emp in self:
            if emp.gender == 'male':
                emp.phone = '+911234567890'
                emp.email = 'abc@gmail.com'
                # return res
            elif emp.gender == 'female':
                emp.phone = '+919874563210'
                emp.email = 'xyz@gmail.com'
                # TODO: In hrms_14 If we already select OPR and than change to female then id is there??

    # TODO 4.8. Add an onchange method for multiple fields to update another field’s value.
    #           NOTE: Here the same method should be called when you change any of the fields.
    #      4.10. If there is no value passed raise a warning in an onchnage method.
    @api.onchange('gender', 'marital_status')
    def incentive_amt(self):
        for emp in self:
            res = {}
            if emp.gender == 'male' and emp.marital_status == 'single':
                emp.incentive = 800.0
            elif emp.gender == 'female' and emp.marital_status == 'single':
                emp.incentive = 900.0
            elif emp.gender == 'male' or emp.gender == 'female' and emp.marital_status == 'married':
                emp.incentive = 1200.0
            # if not emp.marital_status:
            #     res['warning'] = {
            #         'title': 'Marital Status',
            #         'message': 'Marital Status can not be empty.'
            #     }
            return res

    # TODO: 4.9. Add an onchange method which will add a domain on a many2one and
    #            many2many field. Not completed
    @api.onchange('department_id')
    def dept_skill(self):
        res = {'skill_ids': []}
        print('res===============>:', res)
        if self.department_id.id == 2:
            res['domain'] = {'skill_ids': [('name', 'not in', ['Six Sigma'])]}
        else:
            res['domain'] = {'skill_ids': []}
        return res
        # print("self==========>:", self)
        # for emp in self:
        #     print("emp********: ", emp.department_id)  # team.department(2,) this gives me recordset
        #     print("emp.id********: ", emp.department_id.id)  # 2, this gives me id
        #     if emp.department_id.id == 2:
        #         res['domain'] = {'skill_ids': [('name', 'not in', ['Six Sigma'])]}
        #         print("res:", res)
        #     return res


class Department(models.Model):
    _name = 'team.department'
    _description = 'Department'

    _rec_name = 'dep_name'

    # TODO: 4.11.Add an SQL constraint to add a unique constraint on a single field.
    #       4.12. Add an SQL constraint to add a unique constraint on a combination of two fields.
    _sql_constraints = [
        # ('unique_dept_code', 'unique(dep_code)', 'Each department should have unique code'),
        ('unique_dept_name_code', 'unique(dep_name, dep_code)', 'combination of department name and code must be unique')
    ]

    dep_name = fields.Char('Department Name')
    dep_code = fields.Char('Code', size=4)

    # TODO: 4.1. Override name_get method and display two fields rather than just name in the
    #            many2one field.
    def name_get(self):
        """
        To get department name combining with their code.
        :return: List of tuple containing id, name => [(id, name)]
        """
        dept_list = []
        for department in self:
            if department.dep_code:
                dept_list.append((department.id, '[' + department.dep_code + '] ' + department.dep_name))
        return dept_list

    # TODO: 4.2. Override name_search method to search with both the fields which are displayed
    #            in many2one field.
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args += ['|', ('dep_name', operator, name), ('dep_code', operator, name)]
        return self.search(args).name_get()

    # TODO: 4.3. Override name_create method to add additional fields for creating records.
    @api.model
    def name_create(self, name):
        if name:
            code = name[:3].upper()  # TODO: Put logic like for Certi Main Tech we get CMT
            dept_vals = {'dep_name': name, 'dep_code': code}
            return self.create([dept_vals]).name_get()[0]

    # TODO: 4.5. Override fields_view_get method to change the attributes of specific field in a
    #            specific view. For e.g. Change the sortable attribute for a field to False for tree
    #            view. ONly for bydef = Flase
    # TODO 4.6. Override fields_view_get method to change the attribute of a field in all the views.
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Department, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                      toolbar=toolbar, submenu=submenu)
        # print('res==========>', res)
        print("View: ", view_type)
        # print('arch: ', res['arch'])
        print('fields: ', res['fields'])
        print('sortable:', res['fields']['dep_name']['sortable'])

        if view_type == 'tree':
            # res['fields']['dep_name']['store'] = False
            # TODO: Why it's not working if I set store = False, for sortable and searchable.
            #     Solution: This will not working because it only works for records store
            #               which is by default False, not for default store = True.
            res['fields']['dep_name']['sortable'] = False
            print('=' * 30)
            print('View Type: ', view_type)
            print('For tree view sortable:', res['fields']['dep_name']['sortable'])
            print('=' * 30)

        # print('Update Fields: ', res['fields'])
        # print('For tree view sortable:', res['fields']['dep_name']['sortable'])

        if res['fields'].get('dep_name', False):
            res['fields']['dep_name']['required'] = True
        print('Updated fields: ', res['fields'])
        return res


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
