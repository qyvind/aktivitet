from ._anvil_designer import TrekningerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime  # Importer datetime for å håndtere datoer
from datetime import timedelta
from anvil import tables
from anvil.tables import app_tables, query as q
from anvil.users import get_user

class Trekninger(TrekningerTemplate):
  def __init__(self, aktiv_mandag=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Hvis ikke mandag er sendt inn, bruk dagens uke
    if aktiv_mandag is None:
      idag = datetime.date.today()
      aktiv_mandag = idag - datetime.timedelta(days=idag.weekday())  # Finn mandagen i uken

    # Kall serverfunksjonen med aktiv mandag
    liste = self.hent_ukens_premietrekning(aktiv_mandag)
    
    self.trekningsliste_repeating_panel.items = [{"navn": navn} for navn in liste]

  def lukk_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Loggbok")

  def hent_ukens_premietrekning(self,mandag):
    søndag = mandag + timedelta(days=6)
    deltager_dager = {}

    aktiviteter = app_tables.aktivitet.search(
        dato=q.between(mandag, søndag),
        poeng=q.greater_than_or_equal_to(1)
    )

    for rad in aktiviteter:
        deltager = rad['deltager']
        dato = rad['dato']
        if deltager:
            if deltager not in deltager_dager:
                deltager_dager[deltager] = set()
            deltager_dager[deltager].add(dato)

    kvalifiserte = [d for d, dager in deltager_dager.items() if len(dager) >= 5]

    resultat = []
    for deltager in kvalifiserte:
        userinfo = app_tables.userinfo.get(user=deltager)
        navn = userinfo['navn'] if userinfo else deltager['email']
        resultat.append(navn)

    return resultat

  def button_1_click(self, **event_args):
    open_form('Supertrekning')
