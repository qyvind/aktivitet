from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email_label.text = self.item['email']
    self.navn_label.text = self.item['navn']
    self.poeng_label.text = self.item['poeng']
    #self.team_label.text = self.item['team']

    team_list = [row['team'] for row in app_tables.team.search() if row['team']]
    self.team_drop.items = [("", "")] + [(team, team) for team in team_list]

    # Sikre at verdien er i listen, ellers sett den til ""
    selected_team = self.item['team'] if self.item['team'] in team_list else ""

    self.team_drop.selected_value = selected_team

  def slett_bruker_click(self, **event_args):
    """This method is called when the button is clicked"""
    melding = anvil.server.call('delete_user_by_email', self.email_label.text)
    alert(melding)
    parent_form = self.parent
    while parent_form and not hasattr(parent_form, 'bruker_repeating_panel'):
        parent_form = parent_form.parent  # Gå oppover i UI-hierarkiet
    if parent_form and hasattr(parent_form, 'bruker_repeating_panel'):
        # Hent nye data fra databasen
        liste = anvil.server.call('hent_poengsummer')
        parent_form.bruker_repeating_panel.items = liste
      
    
    
    #open_form('admin')

  def save_team_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('update_user_team',self.email_label.text,self.team_drop.selected_value, self.admin_checkbox.checked)




    
