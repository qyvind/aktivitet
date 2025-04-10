from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..VelgIkon import VelgIkon


class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None, callback=None, **properties):
        self.init_components(**properties)
        self.ukedag_label.text = ukedag
        self.callback = callback # Keep this if PoengVelger itself is called with a callback

        # Store the selected icon media object separately
        self.selected_ikon_media = ikon

        self.poeng_drop.items = [
            ("0 poeng", 0),
            ("1 poeng", 1),
            ("2 poeng", 2),
            ("3 poeng", 3)
        ]
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        if self.aktivitet_box.text == "Hviledag":
            self.aktivitet_box.text = ""
        self.beskrivelse.text = beskrivelse

        # --- Remove or comment out the ikon_dropdown setup ---
        # ikon_rader = app_tables.files.search()
        # ikoner = [(rad['path'], rad['file']) for rad in ikon_rader if rad['file']]
        # ikoner.insert(0, ("Ingen ikon", None))
        # self.ikon_dropdown.items = ikoner
        # self.ikon_dropdown.include_placeholder = False
        # self.ikon_dropdown.visible = False # Hide the dropdown if replacing
        # --- End of removal ---

        # Set initial preview from the passed 'ikon' (which is now stored in self.selected_ikon_media)
        self.ikon_preview.source = self.selected_ikon_media

    # --- Remove or comment out ikon_dropdown_change ---
    # def ikon_dropdown_change(self, **event_args):
    #     valgt = self.ikon_dropdown.selected_value
    #     if valgt:
    #         self.ikon_preview.source = valgt
    #         self.selected_ikon_media = valgt # Update if using dropdown too
    #     else:
    #         self.ikon_preview.source = None
    #         self.selected_ikon_media = None
    # --- End of removal ---

    def lagre_button_click(self, **event_args):
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        # Use the stored icon media object
        ikon = self.selected_ikon_media
        beskrivelse = self.beskrivelse.text

        if self.callback:
            # Pass the selected data back using the original callback
            self.callback(poeng, aktivitet, ikon, beskrivelse)

        # Decide how to close/navigate away from PoengVelger
        # If PoengVelger was opened by another form using alert(), use:
        # self.raise_event('x-close_alert', value=True) # Or some value indicating success
        # If it's a main form, navigate elsewhere:
        open_form('Loggbok') # Or wherever it should go

    def ikon_preview_mouse_down(self, x, y, button, keys, **event_args):
        """This method is called when the ikon_preview image is clicked"""
        # Create an instance of the VelgIkon form
        ikon_selector_form = VelgIkon() # No callback needed here

        # Open VelgIkon as a modal dialog using alert()
        # It will pause execution here until VelgIkon is closed
        selected_icon = alert(
            content=ikon_selector_form,
            title="Velg Ikon",
            large=True,
            buttons=[] # Use custom closing mechanism within VelgIkon
        )

        # Code resumes here after the alert closes
        if selected_icon is not None:
            # User selected an icon (selected_icon is the Media object)
            self.selected_ikon_media = selected_icon
            self.ikon_preview.source = self.selected_ikon_media
        # else: user cancelled (selected_icon is None), do nothing