from ._anvil_designer import SessionOverTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import ModuleGlobal


class SessionOver(SessionOverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.answers = app_tables.answers.search(session=ModuleGlobal.session_uuid)

        total_right = 0
        total_wrong = 0
        for answer in self.answers:
            if answer["got_it_right"]:
                total_right += 1
            else:
                total_wrong += 1

        self.total_right = total_right
        self.total_right_percent = total_right / len(self.answers) * 100
        self.total_wrong = total_wrong
        self.total_wrong_percent = total_wrong / len(self.answers) * 100

        self.label_correct.text = f"Correct answers: {str(self.total_right)} - {self.total_right_percent:.2f}%"
        self.label_incorrect.text = f"Incorrect  answers: {str(self.total_wrong)} - {self.total_wrong_percent:.2f}%"
        self.label_total = f"Total of questions answered: {len(self.answers)}"
