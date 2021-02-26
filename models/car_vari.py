from odoo import models, fields, api


class CarVariants(models.Model):

    _name = 'car.variant'
    _description = 'Different variant of Cars'
    _rec_name = 'car_vari'

    car_id = fields.Many2one('car.model',
                             delegate=True,
                             ondelte='cascade',
                             auto_join=True,
                             required=True)

    car_name = fields.Char('Car Name')
    car_vari = fields.Char('Variant')
    fuel = fields.Selection([('gas', 'Gas'),
                             ('petrol', 'Petrol'),
                             ('diesel', 'Diesel'),
                             ('diesel-addblue', 'Diesel With AddBlue'),
                             ('ev', 'EV')])
    # make_year = fields.Date('Make Year')  # options="{'datepicker' : {'showType': 'years'}}"
