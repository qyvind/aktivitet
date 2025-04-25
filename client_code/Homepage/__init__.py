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
    open_form('Loggbok')

  def reusltater_button_click(self, **event_args):
    open_form('Resultat_individuell')

  def regler_button_click(self, **event_args):
    open_form('Regler')

  def trekninger_click(self, **event_args):
    open_form('Trekninger')

  def admin_button_click(self, **event_args):
    open_form('admin')

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')
