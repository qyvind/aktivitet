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
import json


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
    if self.enkeltbruker_card.visible:
      self.enkeltbruker_card.visible = False
      self.team_card.visible=False
      self.bruker_card.visible = False 
      self.konk_card.visible=False
    else:
      self.enkeltbruker_card.visible = True
      self.import_mang_card.visible = False
      self.team_card.visible=False
      self.bruker_card.visible = False 
      self.konk_card.visible=False


  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    anvil.server.call('create_user',self.epost_box.text,self.navn_box.text,self.passord_box.text,self.team_drop.selected_value)

  def import_mang_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.import_mang_card.visible:
      self.import_mang_card.visible = False
      self.team_card.visible=False
      self.bruker_card.visible = False 
      self.konk_card.visible=False
    else:
      self.import_mang_card.visible = True
      self.enkeltbruker_card.visible = False
      self.team_card.visible=False
      self.bruker_card.visible = False 
      self.konk_card.visible=False

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    user_list = json.loads(self.users_label.text)  # Konverter JSON-strengen til en liste
    anvil.server.call('batch_create_users', user_list)

  def teams_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    team_resultater = anvil.server.call('hent_team_poengsummer')
    self.team_repeating_panel.items = team_resultater
    if self.team_card.visible:
      self.team_card.visible=False
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False
      self.bruker_card.visible = False 
      self.konk_card.visible=False
    else:
      self.team_card.visible=True
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False
      self.bruker_card.visible = False 
      self.konk_card.visible=False

  def label1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def Opprett_team_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.nytt_team_box.text != "":
      anvil.server.call('opprett_nytt_team',self.nytt_team_box.text)
      self.nytt_team_box.text = ""
      team_resultater = anvil.server.call('hent_team_poengsummer')
      self.team_repeating_panel.items = team_resultater

  def brukere_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.bruker_card.visible:
      self.bruker_card.visible = False
      self.team_card.visible=False
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False
      self.konk_card.visible=False
    else:
      self.bruker_card.visible = True
      self.team_card.visible=False
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False
      self.konk_card.visible=False
    liste = anvil.server.call('hent_poengsummer')
    self.bruker_repeating_panel.items = liste
    

  def konk_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    konkurransenavn, konkurranse_fradato, konkurranse_tildato = self.hent_konkurranse_info()
    self.konkurransenavn_label.text = konkurransenavn
    self.fra_date_picker.date = konkurranse_fradato
    self.til_date_picker.date = konkurranse_tildato
    self.fra_date_picker.format = "%d/%m-%y"
    self.til_date_picker.format = "%d/%m-%y"
    if self.konk_card.visible:
      self.konk_card.visible=False
      self.bruker_card.visible = False
      self.team_card.visible=False
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False
    else:
      self.konk_card.visible=True
      self.bruker_card.visible = False
      self.team_card.visible=False
      self.import_mang_card.visible = False
      self.enkeltbruker_card.visible = False

  def hent_konkurranse_info(self):
      # Kall serverfunksjonen for å hente den første posten
      record = anvil.server.call('hent_konkurranse')
      # Dersom record finnes, trekk ut feltene og returner dem
      if record:
          konkurransenavn = record['konkurransenavn']
          fradato = record['fradato']
          tildato = record['tildato']
          return konkurransenavn, fradato, tildato
      else:
          return None, None, None

  def lagre_konkurranse_button_click(self, **event_args):
    anvil.server.call('lagre_konkurranse',self.konkurransenavn_label.text,self.fra_date_picker.date,self.til_date_picker.date)
    

      



  


