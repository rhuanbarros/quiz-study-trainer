from ._anvil_designer import ShowQuestionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ShowQuestion(ShowQuestionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    # question = app_tables.questions.search()[0]
    question = anvil.server.call('get_question')
    self.label_question.text = question['question']
    self.label_subject_matter.text = question['title']
    self.label_level.text = question['level']
