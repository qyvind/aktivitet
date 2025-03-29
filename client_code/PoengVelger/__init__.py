from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PoengVelger(PoengVelgerTemplate):
  def __init__(self, valgt_poeng=1, aktivitet="", **properties):
    self.init_components(**properties)
    self.poeng_drop.items = [
      ("= poeng",0),
      ("1 poeng", 1),
      ("2 poeng", 2),
      ("3 poeng", 3)
    ]
    self.poeng_drop.selected_value = valgt_poeng
    self.aktivitet_box.text = aktivitet

  def lagre_button_click(self, **event_args):
      print("Klikket lagre!")
  
      # Returner dataen via `anvil.Alert.OK`
      alert_return_value = {
          "poeng": self.poeng_drop.selected_value,
          "aktivitet": self.aktivitet_box.text
      }
  
      # Bruk standardknappen til å lukke alert og sende verdien
      self.parent.raise_event("x-close", value=anvil.Alert.OK(alert_return_value))
  
    


    

