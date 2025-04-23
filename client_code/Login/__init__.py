from ._anvil_designer import LoginTemplate
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
from ..Utils import Utils


class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Globals.bruker = anvil.users.get_user()
    Globals.userinfo_record = Utils.hent_brukernavn()
    
    if Globals.bruker:
        open_form('Loggbok')
    

    # Any code you write here will run before the form opens.

  def login_click(self, **event_args):
    Globals.bruker = anvil.users.login_with_form()
    if Utils.is_admin():
      Globals.admin=True
    if Globals.bruker:
        open_form('Loggbok')
