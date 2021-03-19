{
    'name': 'Workshop Management',
    'description': 'A module used to manage workshop employees information',
    'version': '1.0',
    'author': 'k&K motors Pvt. Ltd.',
    'website': 'www.knk.com',
    'depends': ['base', 'mail'],
    # for dependency `base` must me there rest if your using some other modules than mention here
    'data': [
        'security/wrks_security.xml',  # path: folder_name/file_name, keep security on the top
        'security/ir.model.access.csv',
        'data/team_sequence.xml',
        'views/wrksp_templates.xml',
        'views/wrks_view.xml',
        'views/update_field_wizard.xml',
        'views/update_salary_wizard_view.xml',
        'views/update_exp_wiz_view.xml',
        'views/team_analysis_report_view.xml',
        'views/workshop_qweb_reports.xml',
        'views/parser_qweb_report_team_template.xml',
        'views/qweb_report_wizard.xml',
        'views/qweb_report_wiz_multy_field_view_template.xml',
        'views/qweb_report_wiz_multy_field_view.xml',
        'views/xls_report_team_wiz_view.xml',
    ],
    'auto_install': False,
    'application': True  # True means it shows as a application not as a supporting module
}