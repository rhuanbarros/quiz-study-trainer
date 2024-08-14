from ._anvil_designer import ShowQuestionTemplate
from anvil import *
import anvil.users
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
    self.get_question()
    
  def get_question(self):
    self.column_panel_btnsanswer.visible = True
    self.linear_panel_explanation.visible = False
    
    self.question = anvil.server.call('get_question')
    self.label_question.text = self.question['question']
    self.label_subject_matter.text = self.question['title']
    self.label_level.text = self.question['level']

    

  def verify_answer(self, answer: bool):
    if answer == bool(self.question['answer_correct']):
      alert("You got it right!")
    else:
      alert("You got it wrong!")

    anvil.server.call('save_answer', answer, self.question )

    self.column_panel_btnsanswer.visible = False
    self.linear_panel_explanation.visible = True

    self.label_explanation.text = self.question['explanation']
    

  def button_true_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.verify_answer(True)

  def button_false_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.verify_answer(False)

  def button_next_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.get_question()
