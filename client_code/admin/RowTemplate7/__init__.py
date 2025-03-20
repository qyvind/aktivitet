from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email_label.text = self.item['email']
    self.navn_label.text = self.item['navn']
    self.poeng_label.text = self.item['poeng']
    self.team_label.text = self.item['team']

  def slett_bruker_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('delete_user_by_email', self.email_label.text)
    open_form('admin')
    
