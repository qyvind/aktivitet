from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""

  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.raise_event('x-edit-aktivitet', aktivitet=self.item)

  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.raise_event('x-delete-aktivitet',aktivitet=self.item)
