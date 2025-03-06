from ._anvil_designer import AktivitetTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ..Edit_Aktivitet import Edit_Aktivitet


class Aktivitet(AktivitetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.aktivitet_card.visible=False
    #self.repeating_panel_1.items = app_tables.aktivitet.search()
    self.repeating_panel_1.add_event_handler('x-edit-aktivitet', self.edit_aktivitet)
    self.repeating_panel_1.add_event_handler('x-delete-aktivitet', self.delete_aktivitet)

    # Any code you write here will run before the form opens.

  def add_aktivitet_button_click(self, **event_args):
    item = {}
    editing_form = Edit_Aktivitet(item=item)
    item['deltager']= anvil.users.get_user()  
    if alert(content=editing_form, large=True):
      anvil.server.call('add_aktivitet', item)
      self.repeating_panel_1.items = app_tables.aktivitet.search(deltager = anvil.users.get_user()  )

  def edit_aktivitet(self, aktivitet, **event_args):
    item = dict(aktivitet)
    editing_form = Edit_Aktivitet(item=item)
    if alert(content=editing_form, large=True):
      #pass in the Data Table row and the updated info
      anvil.server.call('update_aktivitet', aktivitet, item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.aktivitet.search(deltager = anvil.users.get_user()  )

  def delete_aktivitet(self, aktivitet, **event_args):
    if confirm(f"Vil du virkelig slette denne aktiviteten: {aktivitet['aktivitet']}?"):
      anvil.server.call('delete_aktivitet', aktivitet)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.aktivitet.search(deltager = anvil.users.get_user()  )

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form(allow_remembered=30, allow_cancel=True)
    self.repeating_panel_1.items = app_tables.aktivitet.search(deltager = anvil.users.get_user()  )
    if anvil.users.get_user(allow_remembered=30) is not None:
      self.login_button.visible = False
      self.Logout_button.visible = True
      self.aktivitet_card.visible = True

  def Logout_button_click(self, **event_args):
    anvil.users.logout()
    self.login_button.visible = True
    self.Logout_button.visible = False
    self.aktivitet_card.visible = False
    
