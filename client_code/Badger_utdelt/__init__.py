from ._anvil_designer import Badger_utdeltTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Badger_utdelt(Badger_utdeltTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = [
      {
        "email": row["user"]["email"], 
        "badge_name": row["badge"]["name"], 
        "awarded_date": row["awarded_date"], 
        "informert": row["informert"]
      }
      for row in app_tables.user_badges.search()
    ]
    #print(self.items)
