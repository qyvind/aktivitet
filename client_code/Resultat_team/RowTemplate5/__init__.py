from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.team_label.text = self.item['team']
    self.poeng_label.text = self.item['poengsum']

    if self.item['members'] < 3:
      self.members_label.foreground = "red"  # Sett tekstfargen til rød
    else:
      self.members_label.foreground = "black"  # Vanlig farge

    # Any code you write here will run before the form opens.
