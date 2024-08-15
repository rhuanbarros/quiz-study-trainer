from ._anvil_designer import StudyReportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StudyReport(StudyReportTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.layout.reset_links()
        self.layout.link_study_report.role = "selected"
