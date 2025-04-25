from ._anvil_designer import Resultat_team_oldTemplate
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


class Resultat_team_old(Resultat_team_oldTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    team_resultater = Utils.hent_team_poengsummer()
    self.team_resultat_repeating_panel.items = team_resultater
    
    # Any code you write here will run before the form opens.

  def lukk_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Loggbok")

  def button_1_click(self, **event_args):
    open_form('Resultat_individuell')
