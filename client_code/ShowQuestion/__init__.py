from ._anvil_designer import ShowQuestionTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime
import uuid


class ShowQuestion(ShowQuestionTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.current_user = anvil.users.get_user()
        self.session_uuid = str(uuid.uuid4())

        print("self.session_uuid")
        print(self.session_uuid)

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.get_question()

    def get_question(self):
        self.column_panel_btnsanswer.visible = True
        self.linear_panel_explanation.visible = False

        # self.question = anvil.server.call('get_question')
        self.questions = app_tables.questions.search()
        self.question = self.questions[0]

        self.label_question.text = self.question["question"]
        self.label_subject_matter.text = self.question["title"]
        self.label_level.text = self.question["level"]

    def verify_answer(self, answer: bool):
        if answer == bool(self.question["answer_correct"]):
            # alert("You got it right!")
            self.headline_right.visible = True
            self.headline_wrong.visible = False
        else:
            # alert("You got it wrong!")
            self.headline_right.visible = False
            self.headline_wrong.visible = True

        # anvil.server.call("save_answer", answer, self.question)
        app_tables.answers.add_row(
            created_at=datetime.now(),
            question=self.question,
            got_it_right=answer == bool(self.question["answer_correct"]),
            session=self.session_uuid,
            user=self.current_user,
        )

        self.column_panel_btnsanswer.visible = False
        self.linear_panel_explanation.visible = True

        self.label_explanation.text = self.question["explanation"]

    def button_true_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.verify_answer(True)

    def button_false_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.verify_answer(False)

    def button_next_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.get_question()
