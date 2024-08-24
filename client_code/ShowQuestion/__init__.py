from ._anvil_designer import ShowQuestionTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime
import uuid
import random

from .. import ModuleGlobal


class ShowQuestion(ShowQuestionTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.current_user = anvil.users.get_user()
        # self.session_uuid = str(uuid.uuid4())
        # ModuleGlobal.session_uuid = self.session_uuid

        # print("self.session_uuid")
        # print(self.session_uuid)

        self.get_question()

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        # self.card_explanation_elaborate_more.visible = False
        # self.get_question()

    def get_question(self):
        print("get_question")

        self.column_panel_btnsanswer.visible = True
        self.linear_panel_explanation.visible = False
        self.card_explanation_elaborate_more.visible = False

        if len(ModuleGlobal.questions) == 0:
            # session is over
            alert("There is no questions anymore.")
            open_form("SessionSettings")
        else:
            self.question = ModuleGlobal.questions.pop()

            self.label_question.text = self.question["question"]
            self.label_subject_matter.text = (
                "Subject matter title: " + self.question["title"]
            )
            self.label_level.text = "Level: " + self.question["level"]

    def verify_answer(self, answer: bool):
        answer_db_correct_fixed = (
            True
            if self.question["type"] == "true_or_false"
            and self.question["answer_correct"] == "TRUE"
            else False
        )

        if answer == answer_db_correct_fixed:
            # alert("You got it right!")
            self.headline_right.visible = True
            self.headline_wrong.visible = False
        else:
            # alert("You got it wrong!")
            self.headline_right.visible = False
            self.headline_wrong.visible = True

        # jsut for test pourposes
        # if self.current_user is None:
        #     self.current_user = app_tables.users.search()[0]

        app_tables.answers.add_row(
            created_at=datetime.now(),
            question=self.question,
            got_it_right=answer == answer_db_correct_fixed,
            session=self.session_uuid,
            user=self.current_user,
        )

        self.show_answer()

    def show_answer(self):
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

    def button_endsession_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("SessionOver")

    def button_idontknow_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.headline_right.visible = False
        self.headline_wrong.visible = False
        self.show_answer()

    def button_elaboratemore_click(self, **event_args):
        """This method is called when the button is clicked"""
        explanation_elaborate_more = anvil.server.call(
            "elaborate_more", self.question["question"]
        )
        self.card_explanation_elaborate_more.visible = True
        self.label_explanation_elaborate_more.text = explanation_elaborate_more
