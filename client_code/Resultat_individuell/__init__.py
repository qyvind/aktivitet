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
    
    team_resultater = Utils.hent_team_poengsummer()
    self.team_resultat_repeating_panel.items = team_resultater
    self.tabs_1.active_background = "#2196F344"
  




  def button_1_click(self, **event_args):
    open_form('Resultat_team')

  def tabs_1_tab_click(self, tab_index, tab_title, **event_args):
    if tab_title == "Individuell":
      self.individuell_card.visible = True 
      self.team_card.visible=False 
    elif tab_title == "Team":

      self.team_card.visible=True       
      self.individuell_card.visible = False 
