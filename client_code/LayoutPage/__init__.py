from ._anvil_designer import LayoutPageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class LayoutPage(LayoutPageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        anvil.users.login_with_form()

        # ok
        # open_form("SessionSettings") didnt work

    def link_about_us_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("AboutUs")

    def link_generate_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("GenerateQuestions")

    def reset_links(self, **event_args):
        self.link_session_settings.role = ""
        self.link_generate.role = ""
        self.link_study_report.role = ""
        self.link_about_us.role = ""

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        pass

    def link_session_settings_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("SessionSettings")

    def link_study_report_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("StudyReport")
