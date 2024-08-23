from ._anvil_designer import SessionSettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import ModuleGlobal


class SessionSettings(SessionSettingsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""

        # code to set the menu on the layout page
        self.layout.reset_links()
        self.layout.link_session_settings.role = "selected"

        self.get_titles()

    def get_titles(self):
        subject_matter_distinct = (
            row["title"] for row in app_tables.question_titles.search()
        )

        self.drop_down_subject_matter.items = ["All"]
        self.drop_down_subject_matter.items += subject_matter_distinct

    def button_start_click(self, **event_args):
        """This method is called when the button is clicked"""
        ModuleGlobal.subject_matter_selected = (
            self.drop_down_subject_matter.selected_value
        )
        open_form("ShowQuestion")

    def button_update_click(self, **event_args):
        """This method is called when the button is clicked"""

        app_tables.question_titles.delete_all_rows()

        subject_matter_distinct = set(
            (row["title"] for row in app_tables.questions.search())
        )

        for row in subject_matter_distinct:
            app_tables.question_titles.add_row(title=row)

        self.get_titles()
