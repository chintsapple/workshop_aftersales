from odoo import models, fields, api
import xlsxwriter, base64

# TODO: 8.9. Create an Excel report with Some details from your model. Also add some details
#            from wizard’s form.
#      N8.10. Add an image in the Excel report.
#       8.11. Format the report such that the headers are bold.
#       8.12. Merge few columns on the top most rows and put a Title for the report and it must
#             be in the center of the information printed.
#       8.13. Print information of O2M field in the Excel file. Get a total vertically and
#             horizontally in separate cells. Make sure that the data is in bold format.
#      N8.14. Print a Graph in the Excel report with the numeric information that you have
#             printed with your O2M field.


class TeamReportXlsWiz(models.TransientModel):

    _name = 'team.report.xls.wiz'
    _description = 'Excel Report of Team'

    date = fields.Date('Date', default=fields.Date.today())
    house_rent_allowance = fields.Integer('House Rent Allowance', default=15000.0)
    department_id = fields.Many2one('team.department', 'Department')
    employee_ids = fields.Many2many('team.team', string='Team')

    @api.onchange('department_id')
    def onchange_dept(self):
        res = {}
        if self.department_id:
            self.employee_ids = [(5, 0, 0)]
            res['employee_ids'] = {
                'domain': [('department_id', '=', self.department_id.id)]
            }
        else:
            res['employee_ids'] = {
                'domain': []
            }
        return res

    def print_xls_report(self):
        """
        Print Excel report Salary Slip for Employee's.
        """
        team_obj = self.env['team.team']
        attach_obj = self.env['ir.attachment']
        teams = self.employee_ids

        if not teams:
            if self.department_id:
                team_dom = [('department_id', '=', self.department_id.id)]
            else:
                team_dom = []
            teams = team_obj.search(team_dom)

        # Workbook
        workbook = xlsxwriter.Workbook('/tmp/Team Report.xlsx')

        for emp in teams:

            # Worksheet
            worksheet = workbook.add_worksheet(emp.name)
            bold_format = workbook.add_format({'bold': 1})
            normal_format = workbook.add_format({'bold': 0})
            bold_blue_format = workbook.add_format({'bold': 1, 'font_color': 'blue'})

            # 4. Writing the Header
            worksheet.merge_range(4, 4, 5, 6, 'Team Report', bold_blue_format)  # merge cell

            # 5. Writing other data, writing data into cell
            worksheet.write(6, 0, 'Date', bold_format)
            worksheet.write(6, 1, fields.Date.today(), normal_format)

            worksheet.write(7, 0, 'Name', bold_format)
            worksheet.write(7, 1, emp.name, normal_format)

            worksheet.write(8, 0, 'Department', bold_format)
            worksheet.write(8, 1, emp.department_id.dep_name, normal_format)

            worksheet.write(9, 0, 'Month', bold_format)
            worksheet.write(9, 1, 'Basic', bold_format)
            worksheet.write(9, 2, 'Allowance', bold_format)
            worksheet.write(9, 3, 'Gross', bold_format)
            worksheet.write(9, 4, 'Deduction', bold_format)
            worksheet.write(9, 5, 'Net', bold_format)

            row = 10
            col = 0

            # 6. Dynamic Lines / Iterative data
            for sal in emp.salary_ids:
                worksheet.write(row, col, sal.month, normal_format)
                worksheet.write(row, col+1, sal.basic, normal_format)
                worksheet.write(row, col+2, sal.allowance, normal_format)
                worksheet.write(row, col+3, sal.gross_sal, normal_format)
                worksheet.write(row, col+4, sal.deduction, normal_format)
                worksheet.write(row, col+5, sal.net_sal, normal_format)
                worksheet.write_formula(row+1, col+1, '=SUM(B11:B18)', bold_format)
                row += 1

        workbook.close()

# TODO 8.15. Make sure that the reports will be opened or downloaded just like our Qweb
#            reports.

        f1 = open('/tmp/Team Report.xlsx', 'rb')
        xls_data = f1.read()
        buf = base64.encodestring(xls_data)
        doc_id = attach_obj.create({'name': '%s.xlsx' % ('Team Report'),
                                    'datas': buf,
                                    'res_model': 'employee.report.xls.wiz'
                                                 'wizard',
                                    'store_fname': '%s.xlsx' % ('Team Report'),
                                    })

        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc_id.id),
                'target': 'current',
                }


