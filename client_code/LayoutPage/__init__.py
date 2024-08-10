from ._anvil_designer import LayoutPageTemplate
from anvil import *


class LayoutPage(LayoutPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_about_us_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('AboutUs')

  def link_generate_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('GenerateQuestions')

  def reset_links(self, **event_args):
    self.link_about_us.role = ''

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    pass

  def link_session_settings_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('SessionSettings')
