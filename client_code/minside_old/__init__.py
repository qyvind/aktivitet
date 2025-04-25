from ._anvil_designer import minside_oldTemplate
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
from .. import Globals


class minside_old(minside_oldTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.fyll_minside()

  def fyll_minside(self, **properties): 
    user = Globals.bruker
    deltagerdata= anvil.server.call("hent_brukernavn")
    
    navn=deltagerdata['navn']
    mitt_team=deltagerdata['team']
    self.user_email_label.text = user['email']
    self.navn_textbox.text = navn
    if deltagerdata['lock']:
      self.locked.icon = 'fa:lock'
      self.team_medlem.text = mitt_team
      self.team_medlem.visible = True
      self.team_drop_down.visible = False
    else:
      self.locked.icon = 'fa:unlock'
      team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]
      self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]
      self.team_drop_down.selected_value = mitt_team
      self.team_medlem.visible = False
      self.team_drop_down.visible = True
    
    

  def angre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Loggbok')

  def lagre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('oppdater_brukernavn_og_team',self.navn_textbox.text,self.team_drop_down.selected_value)
    open_form('Loggbok')

  def nytt_team_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.nytt_team.text = anvil.server.call('opprett_nytt_team',self.nytt_team.text)
    team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]
    self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]

  def locked_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.locked.icon != 'fa:lock':
      resultat = anvil.server.call('laas_eget_team')
      alert(resultat)
      self.fyll_minside()
    
