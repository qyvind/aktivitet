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

        # Bind images to data - This is correct
        self.image_1.source = self.item.get('file1') # Using .get is safer
        self.image_2.source = self.item.get('file2')
        self.image_3.source = self.item.get('file3')
        self.image_4.source = self.item.get('file4')

        # Option 1: Set event handlers in code (using 'click' is often preferred)
        # self.image_1.set_event_handler('click', self.image_click)
        # self.image_2.set_event_handler('click', self.image_click)
        # self.image_3.set_event_handler('click', self.image_click)
        # self.image_4.set_event_handler('click', self.image_click)

        # Option 2: Set the 'click' event for each image in the Anvil Designer
        # to call the 'image_click' method. This is often cleaner.
        # If using the designer, remove the set_event_handler lines above.

        # The print statement for debugging is fine:
        # print("!!Event handlers set for images")


    # This method will handle clicks from ANY of the 4 images
    # if you set the event handler for all of them to point here.
    def image_click(self, **event_args):
        # 'sender' is the component that triggered the event (the specific Image)
        clicked_image_component = event_args['sender']
        selected_media_object = clicked_image_component.source

        if selected_media_object: # Make sure it's not an empty image slot
            print("!!Image clicked:", selected_media_object)
            # Raise the event with the actual Media object as the payload
            # The event name 'x-image-clicked' is good.
            print("!! Raising x-select")
            self.raise_event('x-select', icon=selected_media_object) # Use 'icon' as key
        # else: ignore clicks on empty image slots



  
