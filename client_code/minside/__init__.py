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


class minside(minsideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user = anvil.users.get_user()
    deltagerdata= anvil.server.call("hent_brukernavn")
    navn=deltagerdata['navn']
    mitt_team=deltagerdata['team']
    self.user_email_label.text = user['email']
    
    self.navn_textbox.text = navn
    team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]

    self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]
    self.team_drop_down.selected_value = mitt_team
    

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
    
