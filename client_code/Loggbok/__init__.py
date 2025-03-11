from ._anvil_designer import LoggbokTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Loggbok(LoggbokTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
  
  def update_button_state(self, button, label):
    """Oppdaterer knappens tekst og farge basert på nåværende tilstand"""
    states = {
        "0": ("1", "RED"),
        "1": ("2", "ORANGE"),
        "2": ("3", "GREEN"),
        "3": ("0", "BLACK"),
    }
    
    if button.text == "0":
        """Viser en popup for å spørre om tekst og oppdaterer en label"""
        text_box = TextBox(placeholder="Skriv her...")

        result = anvil.alert(
            content=text_box,
            title="Skriv inn type aktivitet",
            buttons=["OK", "Avbryt"]
        )
    
        if result == "OK":  # Hvis brukeren trykket "OK"
            label.text = text_box.text  # Hent tekst fra TextBox og sett den i riktig label
    
    if button.text in states:
        button.text, button.foreground = states[button.text]
    else:
        print("button not in states")

  def son_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.son_button, self.son_akt_label)
  
  def man_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.man_button, self.man_akt_label)

  def tir_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.tir_button, self.tir_akt_label)

  def ons_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.ons_button, self.ons_akt_label)

  def tor_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.tor_button, self.tor_akt_label)

  def fre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.fre_button, self.fre_akt_label)

  def lor_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.lor_button, self.lor_akt_label)


