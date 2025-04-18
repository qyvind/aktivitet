from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

            # Hent ut data for hvert ikon (hvis det finnes)
    icon_data_1 = self.item.get('icon_1')
    icon_data_2 = self.item.get('icon_2')
    icon_data_3 = self.item.get('icon_3')
    icon_data_4 = self.item.get('icon_4')

    # --- Sett egenskaper for Bilde 1 ---
    if icon_data_1:
        self.image_1.source = icon_data_1.get('media')
        # Hent det pene navnet fra 'path' og sett det som tooltip
        self.label_1.text = icon_data_1.get('path', '') # Bruker .get() for sikkerhets skyld
        self.image_1.tag = icon_data_1 # Lagre hele dictionaryen i tag
    else:
        # Håndter tilfellet der det ikke er noe ikon på denne plassen
        self.image_1.source = None
        self.label_1.text = "" # Ingen tooltip for tom plass
        self.image_1.tag = None

    # --- Sett egenskaper for Bilde 2 ---
    if icon_data_2:
        self.image_2.source = icon_data_2.get('media')
        self.label_2.text = icon_data_2.get('path', '')
        self.image_2.tag = icon_data_2
    else:
        self.image_2.source = None
        self.label_2.text = ""
        self.image_2.tag = None

    # --- Sett egenskaper for Bilde 3 ---
    if icon_data_3:
        self.image_3.source = icon_data_3.get('media')
        self.label_3.text = icon_data_3.get('path', '')
        self.image_3.tag = icon_data_3
    else:
        self.image_3.source = None
        self.label_3.text = ""
        self.image_3.tag = None

    # --- Sett egenskaper for Bilde 4 ---
    if icon_data_4:
        self.image_4.source = icon_data_4.get('media')
        self.label_4.text = icon_data_4.get('path', '')
        self.image_4.tag = icon_data_4
    else:
        self.image_4.source = None
        self.label_4.text = ""
        self.image_4.tag = None




  def image_click(self, x, y, button, keys, **event_args):
        clicked_image_component = event_args['sender']

        selected_icon_data = clicked_image_component.tag

        if selected_icon_data: # Sjekk at vi klikket på et bilde med data
            # selected_icon_data er nå {'media': MediaObject, 'path': 'stien/til/fil.png'}
          

            if self.parent:
                 
              self.parent.raise_event('x-icon-click', icon_data=selected_icon_data, clicked_image=clicked_image_component)

            else:
              print("ItemTemplate1 (Ikon) FEIL: Kunne ikke finne self.parent!")


