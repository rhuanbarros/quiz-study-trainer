from ._anvil_designer import GenerateQuestionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime


class GenerateQuestions(GenerateQuestionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.layout.reset_links()
    self.layout.link_generate.role = 'selected'

  def button_generate_click(self, **event_args):
    """This method is called when the button is clicked"""

    if self.text_area_list_topics.text is None or len(str(self.text_area_list_topics.text)) == 0:
      alert("List of topics shouldn't be empty")
      return
    
    levels = []
    if self.check_box_easy.checked:
      levels.append("easy")
    if self.check_box_medium.checked:
      levels.append("medium")
    if self.check_box_hard.checked:
      levels.append("hard")

    if len(levels) == 0:
      alert("You need to select one option of level.")
      return

    try:
      quantity = int(self.text_box_quantity.text)
    except Exception as e:
      alert("Quantity should be a integer.")
      

    for level in levels:
      print( "Runing code for level:", level )
      
      parameters = {
        "quantity": quantity,
        "level": level,
        "additional_task_description": self.text_area_additional_task_description.text,
        "domain_knowledge": self.text_area_list_topics.text
      }

      anvil.server.call(
        'generate_questions', 
        self.text_box_title.text,
        parameters
      )
      
      alert("Generation completed!")
      
