from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.layout.show_sidesheet = False

    if Globals.admin:
      self.admin_button.visible = True
    else:
      self.admin_button.visible = False

    # Any code you write here will run before the form opens.

  def loggbok_button_click(self, **event_args):
    self.loggbok_button.selected = True
    self.reusltater_button.selected = False
    self.admin_button.selected = False
    self.trekninger_button.selected = False
    self.regler_button.selected = False
    self.min_side_link.selected = False
    

  def reusltater_button_click(self, **event_args):
    self.loggbok_button.selected = False
    self.reusltater_button.selected = True
    self.admin_button.selected = False
    self.trekninger_button.selected = False
    self.regler_button.selected = False
    self.min_side_link.selected = False

  def regler_button_click(self, **event_args):
    self.loggbok_button.selected = False
    self.reusltater_button.selected = False
    self.admin_button.selected = False
    self.trekninger_button.selected = False
    self.regler_button.selected = True
    self.min_side_link.selected = False

  def trekninger_button_click(self, **event_args):
    self.loggbok_button.selected = False
    self.reusltater_button.selected = False
    self.admin_button.selected = False
    self.trekninger_button.selected = True
    self.regler_button.selected = False
    self.min_side_link.selected = False
    
  def admin_button_click(self, **event_args):
    self.loggbok_button.selected = False
    self.reusltater_button.selected = False
    self.admin_button.selected = True
    self.trekninger_button.selected = False
    self.regler_button.selected = False
    self.min_side_link.selected = False
    
  def logout_button_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')

  def min_side_link_click(self, **event_args):
    self.loggbok_button.selected = False
    self.reusltater_button.selected = False
    self.admin_button.selected = False
    self.trekninger_button.selected = False
    self.regler_button.selected = False
    self.min_side_link.selected = True
  def mitt_lag_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    
    
