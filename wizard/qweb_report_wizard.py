from odoo import models, fields, api

# TODO: 8.4. Create a wizard to print the above two reports. Give two buttons on wizard HTML
#            and PDF. If the user clicks on HTML it should open the HTML report else PDF
#            Report.


class QwebReportWizard(models.TransientModel):

    _name = 'qweb.report.wiz'
    _description = 'Wizard to create qweb report HTML or PDF'

    name_id = fields.Many2one('team.team')

    def html_qweb(self):
        # name = self.env['team.team'].search([])  # This will give report for all employees
        name = self.env['team.team'].search([('id', '=', self.name_id.id)])
        return self.env.ref('workshop_aftersales.team_report_html').report_action(name)
        # report_action => Return an action of type ir.actions.report

    def pdf_qweb(self):
        name = self.env['team.team'].search([('id', '=', self.name_id.id)])
        return self.env.ref('workshop_aftersales.team_report_pdf').report_action(name)
