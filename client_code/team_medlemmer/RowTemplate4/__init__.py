from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.navn_label.text = self.item['navn']
    self.poeng_label.text = self.item['poeng']
    

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    user = self.item['user'] 
              
    open_form("BrukerLoggbok", enuser=user)
    
