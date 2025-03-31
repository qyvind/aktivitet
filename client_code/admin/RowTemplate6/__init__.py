from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.team_label.text = self.item['team']
    self.poeng_label.text = self.item['poengsum']
    self.lock.checked = self.item['lock']

    # Any code you write here will run before the form opens.

  def slett_team_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('slett_team',self.team_label.text)
    parent_form = self.parent
    while parent_form and not hasattr(parent_form, 'team_repeating_panel'):
        parent_form = parent_form.parent  # Gå oppover i UI-hierarkiet
    if parent_form and hasattr(parent_form, 'team_repeating_panel'):
        # Hent nye data fra databasen
        team_resultater = anvil.server.call('hent_team_poengsummer')
        parent_form.team_repeating_panel.items = team_resultater
      
