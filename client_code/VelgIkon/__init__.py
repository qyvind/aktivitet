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
    def __init__(self, callback, **properties):
        self.init_components(**properties)
        self.callback = callback

        ikoner = app_tables.files.search()
        
        # Organiser ikonene i grupper på fire
        grupperte_ikoner = []
        for i in range(0, len(ikoner), 4):
            gruppe = {
                'file1': ikoner[i]['file'] if i < len(ikoner) else None,
                'file2': ikoner[i+1]['file'] if i+1 < len(ikoner) else None,
                'file3': ikoner[i+2]['file'] if i+2 < len(ikoner) else None,
                'file4': ikoner[i+3]['file'] if i+3 < len(ikoner) else None,
            }
            grupperte_ikoner.append(gruppe)
        
        # Sett elementene i RepeatingPanel
        self.ikon_repeating_panel.items = grupperte_ikoner

        # Legg til hendelsesbehandler for klikkhendelser
        self.ikon_repeating_panel.set_event_handler('x-image-clicked', self.image_clicked)
        print("!Event handler set for x-image-clicked")

    def image_clicked(self, **event_args):
        print("!Image clicked event received:", event_args['image'])
        # Hent bildet som ble klikket
        clicked_image = event_args['image']
        self.image_1.source = clicked_image
        
        # Bruk callback-funksjonen for å returnere bildet
        self.callback(clicked_image)
        open_form('PoengVelger')