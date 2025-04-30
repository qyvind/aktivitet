from ._anvil_designer import minsideTemplate
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


class minside(minsideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.fyll_minside()

  def fyll_minside(self, **properties): 
    user = Globals.bruker
    deltagerdata= Utils.hent_brukernavn()
    
    self.poeng.text = deltagerdata['poeng']
    self.bonus.text = deltagerdata['bonus']
    self.longest_streak.text = deltagerdata['longest_streak']
    self.score.text = deltagerdata['score']
    antall_deltagere = len(app_tables.userinfo.search())
    self.plassering.text = f"{deltagerdata['plassering']}/{antall_deltagere}"    
    antall_teams =  len(app_tables.team.search())
    self.team_plassering.text = f"{deltagerdata['team_plassering']}/{antall_teams}"
    self.plassering_i_team.text = f"{deltagerdata['plassering_i_team']}/{deltagerdata['team_members']}"
    self.team_score.text = deltagerdata['team_score']
    self.team.text = deltagerdata['team']
    if self.team.text == "" :
      self.team_card.visible=False 
    else:
      self.team_card.visible = True
    
    
    navn=deltagerdata['navn']
    mitt_team=deltagerdata['team']
    #plassering = deltagerdata['plassering']
    self.user_email_label.text = user['email']
    self.navn_textbox.text = navn
    if deltagerdata['lock']:
      self.locked.icon = 'fa:lock'
      self.team_medlem.text = mitt_team
      self.team_medlem.visible = True
      self.team_drop_down.visible = False
      self.lag_team_panel.visible = False 
    else:
      self.locked.icon = 'fa:unlock'
      self.lag_team_panel.visible = True 
      team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]
      self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]
      
      self.team_drop_down.selected_value = mitt_team
      self.team_medlem.visible = False
      self.team_drop_down.visible = True
    team_medl = Utils.hent_teammedlemmer(mitt_team)
    
    self.team_medl_repeating_panel.items = [{"navn": member["navn"], "poeng": member["poeng"],"bonus": member["bonus"], "lengste_streak":member["lengste_streak"],"score":member["score"],"userrecord":member["userrecord"]} for member in team_medl]
      
    

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
    

  def badge_1_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_1.tooltip)
  def badge_2_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_2.tooltip)
  def badge_3_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_3.tooltip)
  def badge_4_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_4.tooltip)
  def badge_5_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_5.tooltip)
  def badge_6_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_6.tooltip)
  def badge_7_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_7.tooltip)
  def badge_8_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_8.tooltip)
  def badge_9_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_9.tooltip)


  def image_mouse_enter(self, x, y, **event_args):
    anvil.js.window.document.body.style.cursor = 'pointer'

  def image_mouse_leave(self, x, y, **event_args):
    anvil.js.window.document.body.style.cursor = 'default'