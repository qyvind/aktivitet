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
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def update_button_state(self, button):
    """Oppdaterer knappens tekst og farge basert på nåværende tilstand"""
    states = {
        "0": ("1", "RED"),
        "1": ("2", "ORANGE"),
        "2": ("3", "GREEN"),
        "3": ("0", "BLACK"),
    }
    
    if button.text in states:
      print(f"Oppdaterer {button} fra {button.text} til {states[button.text]}")
      button.text, button.foreground = states[button.text]
    else:
      print("button not in states")

  def son_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.son_button)
  
  def man_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.man_button)

  def tir_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.tir_button)

  def ons_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.ons_button)

  def tor_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.tor_button)

  def fre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.fre_button)

  def lor_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_button_state(self.lor_button)





  



