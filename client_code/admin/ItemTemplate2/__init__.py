from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.prompt.text = self.item['prompt']

  def prompt_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    def button_lagre_click(self, **event_args):
      ny_tekst = prompt.text
      anvil.server.call('lagre_prompt', self.item, ny_tekst)
      Notification("Prompt lagret!", style="success").show()
