from ._anvil_designer import SessionSettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import ModuleGlobal

import uuid
import random


class SessionSettings(SessionSettingsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.current_user = anvil.users.get_user()
        self.session_uuid = str(uuid.uuid4())
        ModuleGlobal.session_uuid = self.session_uuid

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
        ModuleGlobal.session_revision = False

        # ModuleGlobal.subject_matter_selected = (
        #     self.drop_down_subject_matter.selected_value
        # )

        if self.drop_down_subject_matter.selected_value == "All":
            self.questions = app_tables.questions.search()
        else:
            self.questions = app_tables.questions.search(
                title=self.drop_down_subject_matter.selected_value
            )
        # self.ansers = app_tables.answers.search(question=q.all_of(self.questions))
        self.answers = app_tables.answers.search()

        # print("len(self.questions)")
        # print(len(self.questions))

        if len(self.questions) == 0:
            alert("No questions found")
            return

        # some kind of LEFT JOIN implemention because Anvil doesn't have it in free plan
        self.questions_not_answered_yet = []
        for question in self.questions:
            found_answer = False
            for answer in self.answers:
                same_subject = (
                    answer["question"]["title"] == ModuleGlobal.subject_matter_selected
                )
                same_session = (
                    answer["session"] == self.session_uuid
                )  # i dont want to repeat questions in the same session
                same_user = answer["user"] == self.current_user
                question_already_answered = answer["question"] == question
                if (
                    same_session
                    and same_subject
                    and same_user
                    and question_already_answered
                ):
                    found_answer = True
                    break

            if not found_answer:
                self.questions_not_answered_yet.append(question)

        random.shuffle(self.questions_not_answered_yet)

        # print("len(self.questions_not_answered_yet)")
        # print(len(self.questions_not_answered_yet))

        if len(self.questions_not_answered_yet) == 0:
            alert("No questions found")
            return

        ModuleGlobal.questions = self.questions_not_answered_yet

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

    def button_revision_click(self, **event_args):
        """This method is called when the button is clicked"""
        ModuleGlobal.session_revision = True

        anvil.server.call("get_question_revision")

        open_form("ShowQuestion")
