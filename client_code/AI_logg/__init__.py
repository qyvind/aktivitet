from ._anvil_designer import AI_loggTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AI_logg(AI_loggTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = anvil.server.call('hent_ai_log')
    

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin')
