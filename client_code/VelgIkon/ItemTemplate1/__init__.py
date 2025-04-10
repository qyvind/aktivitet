from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Bind bilder til data
        self.image_1.source = self.item['file1']
        self.image_2.source = self.item['file2']
        self.image_3.source = self.item['file3']
        self.image_4.source = self.item['file4']

        # Legg til klikkhendelser
        self.image_1.set_event_handler('mouse_down', self.image_click)
        self.image_2.set_event_handler('mouse_down', self.image_click)
        self.image_3.set_event_handler('mouse_down', self.image_click)
        self.image_4.set_event_handler('mouse_down', self.image_click)
        print("!!Event handlers set for images")

    def image_click(self, **event_args):
        print("!!Image clicked:", event_args['sender'].source)
        # Hent bildet som ble klikket
        clicked_image = event_args['sender']
        
        
        # Send bildet tilbake til hovedskjemaet
        self.raise_event('x-image-clicked', image=clicked_image.source)
        print("Event raised for x-image-clicked")
