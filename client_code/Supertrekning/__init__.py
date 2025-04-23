from ._anvil_designer import SupertrekningTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime  # Importer datetime for å håndtere datoer
from ..Utils import Utils


class Supertrekning(SupertrekningTemplate):
  def __init__(self, aktiv_mandag=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Hvis ikke mandag er sendt inn, bruk dagens uke
    if aktiv_mandag is None:
      idag = datetime.date.today()
      aktiv_mandag = idag - datetime.timedelta(
        days=idag.weekday()
      )  # Finn mandagen i uken

    # Kall serverfunksjonen med aktiv mandag
      record = Utils.hent_konkurranse()
      if record:
        fradato = record['fradato']
        tildato = record['tildato']
    
    liste = anvil.server.call("hent_konsekutive_kvalifiserte",fradato,tildato)

    self.trekningsliste_repeating_panel.items = [{"navn": navn} for navn in liste]

  def lukk_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Loggbok")

  def button_1_click(self, **event_args):
    open_form('Trekninger')
