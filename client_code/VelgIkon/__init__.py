from ._anvil_designer import VelgIkonTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class VelgIkon(VelgIkonTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Load all icons from the 'files' table
        # Ensure you only get rows where 'file' actually exists
        all_icons = [r['file'] for r in app_tables.files.search() if r['file']]

        # Group icons into lists of 4 for the repeating panel
        grouped_icons = []
        for i in range(0, len(all_icons), 4):
            # Create a dictionary for each row in the repeating panel
            row_data = {
                'icon_1': all_icons[i]   if i < len(all_icons) else None,
                'icon_2': all_icons[i+1] if i+1 < len(all_icons) else None,
                'icon_3': all_icons[i+2] if i+2 < len(all_icons) else None,
                'icon_4': all_icons[i+3] if i+3 < len(all_icons) else None,
            }
            grouped_icons.append(row_data)

        # Set the items for the repeating panel
        self.ikon_repeating_panel.items = grouped_icons
        # --- Explicitly set the handler USING HYPHENATED EVENT NAME ---
        # The first argument is the event name string as raised ('x-icon-selected')
        # The second argument is the actual handler method
        self.ikon_repeating_panel.set_event_handler('x-icon-selected', self.ikon_repeating_panel_x_icon_selected)
        print("! Explicit handler set for 'x-icon-selected'")

        # Any code you write here will run when the form opens.

    # In VelgIkon class
    # *** KEEP THIS HANDLER NAME THE SAME (with underscores) ***
    def ikon_repeating_panel_x_icon_selected(self, icon_media, **event_args):
        """This method is called when the 'x-icon-selected' event is raised by ItemTemplate1"""
        print(f"! Event 'x-icon-selected' received in VelgIkon. Icon: {icon_media.name if icon_media else 'None'}")
        self.raise_event('x_close_alert', value=icon_media)