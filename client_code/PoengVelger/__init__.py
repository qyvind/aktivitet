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


import anvil.server

class PoengVelger(PoengVelgerTemplate):
  def __init__(self, valgt_poeng=1, aktivitet="", ikon=None, ukedag="", **properties):
    self.init_components(**properties)

    self.poeng_drop.items = [
      ("0 poeng", 0),
      ("1 poeng", 1),
      ("2 poeng", 2),
      ("3 poeng", 3)
    ]
    self.poeng_drop.selected_value = valgt_poeng
    self.aktivitet_box.text = aktivitet
    self.ikon_dropdown.items = [
      ("⚽ Fotball", "fa:futbol"),
      ("🏀 Basketball", "fa:basketball"),
      ("⚾ Baseball", "fa:baseball"),
      ("🏐 Volleyball", "fa:volleyball"),
      ("🎾 Tennis", "fa:table-tennis"),
      ("🚴‍♂️ Sykling", "fa:bicycle"),
      ("🏊 Svømming", "fa:swimmer"),
      ("🏋️‍♂️ Styrke", "fa:dumbbell"),
      ("🥊 Boksing", "fa:boxing-glove"),
      ("🏃‍♂️ Jogging", "fa:person-running"),
      ("Ingen ikon", None)
    ]
    self.ikon_dropdown.selected_value = ikon or None

    def lagre_button_click(self, **event_args):
        self.raise_event("x-close", value={
            "poeng": self.poeng_drop.selected_value,
            "aktivitet": self.aktivitet_box.text,
            "ikon": self.ikon_dropdown.selected_value
        })

 

     
    


    

