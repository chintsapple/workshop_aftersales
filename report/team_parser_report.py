from odoo import models, api

# TODO: 8.5. Create a Parser file and define at least 2 methods and use it in the report template.
#       Doubt 8.6. Print Image in the Qweb Report.
#       Doubt 8.7. Print a Barcode for one of the character field of your model in the Qweb Report.


class TeamParserReport(models.AbstractModel):

    _name = 'report.workshop_aftersales.report_team'
    _description = 'Adding Fields while print record'

    @api.model
    def _get_report_values(self, docids, data=None):
        team_obj = self.env['team.team']
        docs = team_obj.browse(docids)

        return {
            'doc_ids': docids,
            'doc_mode;': 'team.team',
            'data': data,
            'docs': docs,
            'sign': 'Signature',
            'get_total_gross': self._get_total_gross,
            'get_ctc': self._get_ctc,
        }

    @api.model
    def _get_total_gross(self, salaries):
        total_gross = 0.0
        for sal in salaries:
            total_gross += sal.gross_sal
        return total_gross

    @api.model
    def _get_ctc(self, salaries):
        # ctc = 0.0
        benefit = 10000.0
        total_gross = 0.0
        for sal in salaries:
            total_gross += sal.gross_sal
        return total_gross + benefit

# TODO 8.8 Parser part, added


class TeamParserReportWiz(models.AbstractModel):

    _name = 'report.workshop_aftersales.report_team_wizard_multi'
    _description = 'Adding Fields while print record'

    @api.model
    def _get_report_values(self, docids, data=None):
        team_obj = self.env['team.team']
        if not docids:
            docids = data['ids']
        print("DOCIDS========>", docids)
        print("DATA==========>", data)
        docs = team_obj.browse(docids)

        return {
            'doc_ids': docids,
            'doc_mode;': 'team.team',
            'data': data,
            'docs': docs,
            'sign': 'Sign',
            'get_total_gross': self._get_total_gross,
            'get_ctc': self._get_ctc,
        }

    @api.model
    def _get_total_gross(self, salaries):
        total_gross = 0.0
        for sal in salaries:
            total_gross += sal.gross_sal
        return total_gross

    @api.model
    def _get_ctc(self, salaries, house_allowance):
        # ctc = 0.0
        benefit = 10000.0
        total_gross = 0.0
        for sal in salaries:
            total_gross += sal.gross_sal
        return total_gross + benefit + house_allowance
