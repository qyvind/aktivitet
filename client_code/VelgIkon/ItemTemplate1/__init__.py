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
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the Item Template is initialized.

        # The 'self.item' property is automatically populated by the RepeatingPanel
        # It contains one dictionary from the 'grouped_icons' list in VelgIkon
        # Use .get() to safely access dictionary keys that might be missing (for the last row)
        self.image_1.source = self.item.get('icon_1')
        self.image_2.source = self.item.get('icon_2')
        self.image_3.source = self.item.get('icon_3')
        self.image_4.source = self.item.get('icon_4')

        # Make sure the 'click' event for image_1, image_2, image_3, image_4
        # is set to call 'image_click' IN THE DESIGNER VIEW

    def image_click(self, **event_args):
        """This method is called when image_1, image_2, image_3, or image_4 is clicked"""
        # 'sender' is the specific Image component that was clicked
        clicked_image_component = event_args['sender']

        # Get the media object assigned to the clicked image's source
        selected_media_object = clicked_image_component.source

        # Only raise the event if a valid media object was clicked (not an empty slot)
        if selected_media_object:
            print(f"!! Image clicked in ItemTemplate1: {selected_media_object.name}")
            # Raise a custom event named 'x_icon_selected' on this item template instance.
            # This event will bubble up to the parent RepeatingPanel (ikon_repeating_panel).
            # Pass the selected media object as a keyword argument.
            self.raise_event('x-icon_selected', icon_media=selected_media_object)
            print("!! Event 'x-icon_selected' raised from ItemTemplate1")
        else:
            print("!! Clicked on an empty image slot.")