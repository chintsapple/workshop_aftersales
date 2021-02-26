{
    'name': 'Workshop Management Pro',
    'description': 'A module used to manage workshop employees information with additional fields',
    'version': '1.0',
    'author': 'k&K motors Pvt. Ltd.',
    'website': 'www.knk.com',
    'depends': ['workshop_aftersales'],
    'data': [
        'security/wrksp_pro_security.xml',
        'security/ir.model.access.csv',
        'views/wrksp_pro_views.xml',
        'views/car_views.xml',
    ],
    'auto_install': False,
    'application': False
}