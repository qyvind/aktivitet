from ._anvil_designer import admin_ny_aktivitetTemplate
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


class admin_ny_aktivitet(admin_ny_aktivitetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    resultat = Utils.hent_ny_aktivitet()
    print(resultat)
    self.repeating_panel_1.items = resultat

  def button_1_click(self, **event_args):
    svar = alert(
        title="Er du sikker?",
        content="Vil du virkelig slette alle forslag til aktiviteter?",
        buttons=[("Ja", True), ("Nei", False)],
        large=True
    )
    
    if svar:
        anvil.server.call('slett_alle_ny_aktivitet')
        alert("Alle aktiviteter er slettet.")
        open_form('admin_ny_aktivitet'
                 )
    else:
        alert("Sletting avbrutt.")
