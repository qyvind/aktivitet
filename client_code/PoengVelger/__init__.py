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
  def __init__(self, valgt_poeng=1, aktivitet="",ukedag="", callback=None, **properties):
    self.init_components(**properties)
    self.ukedag_label.text = ukedag
    
    self.poeng_drop.items = [
      ("0 poeng",0),
      ("1 poeng", 1),
      ("2 poeng", 2),
      ("3 poeng", 3)
    ]
    self.poeng_drop.selected_value = valgt_poeng
    self.aktivitet_box.text = aktivitet
    self.callback = callback  # 👈 Dette tar vare på funksjonen

  def lagre_button_click(self, **event_args):
    poeng = self.poeng_drop.selected_value
    aktivitet = self.aktivitet_box.text

    if self.callback:
        self.callback(poeng, aktivitet)  # 👈 Send data tilbake til Loggbok

    open_form('Loggbok')  # Gå tilbake til hovedform

    
  
     
    


    

