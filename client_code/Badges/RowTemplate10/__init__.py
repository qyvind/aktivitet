from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate10(RowTemplate10Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def badge_prompt_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    anvil.server.call('update_badge',self.item)
