from ._anvil_designer import admin_ny_aktivitet_oldTemplate
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


class admin_ny_aktivitet_old(admin_ny_aktivitet_oldTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    resultat = Utils.hent_ny_aktivitet()
    print(resultat)
    self.repeating_panel_1.items = resultat
