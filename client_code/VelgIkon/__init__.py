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
    # Remove callback from __init__
    def __init__(self, **properties):
        self.init_components(**properties)
        # Remove self.callback = callback

        ikoner = app_tables.files.search()

        grupperte_ikoner = []
        for i in range(0, len(ikoner), 4):
            gruppe = {
                'file1': ikoner[i]['file'] if i < len(ikoner) else None,
                'file2': ikoner[i+1]['file'] if i+1 < len(ikoner) else None,
                'file3': ikoner[i+2]['file'] if i+2 < len(ikoner) else None,
                'file4': ikoner[i+3]['file'] if i+3 < len(ikoner) else None,
            }
            grupperte_ikoner.append(gruppe)

        self.ikon_repeating_panel.items = grupperte_ikoner

        # --- Explicitly set the handler ---
        # The first argument is the event name as raised ('x-select')
        # The second argument is the actual handler method
        self.ikon_repeating_panel.set_event_handler('x-select', self.ikon_repeating_panel_x_select)
        print("! Explicit handler set for x-select") # Add this to confirm it runs


    # Rename the handler method
    def ikon_repeating_panel_x_select(self, icon, **event_args): # Match key 'icon'
        """Handler for x-select event"""
        print("! x-select event received in VelgIkon:", icon)
        self.raise_event('x-close_alert', value=icon)