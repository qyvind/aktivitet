from ._anvil_designer import adminTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class admin(adminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    team_list = [row['team'] for row in app_tables.team.search() if row['team']]
    self.team_drop.items = [("", "")] + [(team, team) for team in team_list]
    self.team_drop.selected_value = "" 

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Loggbok")

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.enkeltbruker_card.visible==True:
      self.enkeltbruker_card.visible = False
    else:
      self.enkeltbruker_card.visible = True
      self.import_mang_card.visible = False

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    anvil.server.call('create_user',self.epost_box.text,self.navn_box.text,self.passord_box.text,self.team_drop.selected_value)

  def import_mang_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.import_mang_card.visible == True:
      self.import_mang_card.visible = False
    else:
      self.import_mang_card.visible = True
      self.enkeltbruker_card.visible = False
      



  


