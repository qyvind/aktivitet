from ._anvil_designer import AktivitetTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ..Edit_Aktivitet import Edit_Aktivitet


class Aktivitet(AktivitetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = app_tables.aktivitet.search()

    # Any code you write here will run before the form opens.

  def add_aktivitet_button_click(self, **event_args):
    item = {}
    editing_form = Edit_Aktivitet(item=item)
      
    if alert(content=editing_form, large=True):
      anvil.server.call('add_aktivitet', item)
      self.repeating_panel_1.items = app_tables.aktivitet.search()
