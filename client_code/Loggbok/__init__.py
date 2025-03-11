from ._anvil_designer import LoggbokTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Loggbok(LoggbokTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def son_0_click(self, **event_args):
    """This method is called when the button is clicked"""

  def man_0_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.man_0.visible=False
    self.man_1.visible=True

  def man_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.man_1.visible=False
    self.man_2.visible=True

  def man_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.man_2.visible=False
    self.man_3.visible=True

  def man_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.man_3.visible=False
    self.man_0.visible=True

