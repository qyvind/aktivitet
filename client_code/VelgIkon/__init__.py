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

        # --- MODIFISERT DEL START ---
        # Load all icons with their paths from the 'files' table
        # Fetch rows that have both 'file' and 'path' populated
        all_icon_data = [{'media': r['file'], 'path': r['path']}
                         for r in app_tables.files.search()
                         if r['file'] and r['path']] # Sørg for at begge feltene finnes

        # Group icon data into lists of 4 for the repeating panel
        grouped_icon_data = []
        for i in range(0, len(all_icon_data), 4):
            # Create a dictionary for each row in the repeating panel
            # Hver 'icon_x' inneholder nå en dictionary med 'media' og 'path'
            row_data = {
                'icon_1': all_icon_data[i]   if i < len(all_icon_data) else None,
                'icon_2': all_icon_data[i+1] if i+1 < len(all_icon_data) else None,
                'icon_3': all_icon_data[i+2] if i+2 < len(all_icon_data) else None,
                'icon_4': all_icon_data[i+3] if i+3 < len(all_icon_data) else None,
            }
            grouped_icon_data.append(row_data)

        self.ikon_repeating_panel.items = grouped_icon_data
        # --- MODIFISERT DEL SLUTT ---

        self.ikon_repeating_panel.add_event_handler('x-icon-click', self.icon_selected)

    def icon_selected(self, icon_data, **event_args):
        """Denne mottar nå en dictionary med 'media' og 'path'"""
        
        self.raise_event('x-close-alert', value=icon_data)
        