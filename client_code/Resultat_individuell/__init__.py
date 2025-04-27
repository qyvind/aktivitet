from ._anvil_designer import Resultat_individuellTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Utils import Utils


class Resultat_individuell(Resultat_individuellTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    liste = Utils.hent_poengsummer_uten_null()
    
    
    self.resultat_repeat_panel.items = liste

    # Any code you write here will run before the form opens.



  def button_1_click(self, **event_args):
    open_form('Resultat_team')

