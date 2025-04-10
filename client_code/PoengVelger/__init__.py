from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# Make sure the import path is correct for your project structure
from ..VelgIkon import VelgIkon

class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None, callback=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Store the callback if this form itself is used modally
        self.callback = callback

        # Store the currently selected icon Media object
        # Initialize with the 'ikon' passed in (could be None)
        self.selected_ikon_media = ikon

        # Set up other fields based on passed parameters
        self.ukedag_label.text = ukedag
        self.poeng_drop.items = [("0 poeng", 0), ("1 poeng", 1), ("2 poeng", 2), ("3 poeng", 3)]
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        if self.aktivitet_box.text == "Hviledag":
            self.aktivitet_box.text = ""
        self.beskrivelse.text = beskrivelse

        # Set the initial icon preview
        self.ikon_preview.source = self.selected_ikon_media

        # Any code you write here will run when the form opens.

    def ikon_preview_click(self, **event_args):
        """This method is called when the ikon_preview Image is clicked."""
        # Create an instance of the icon selection form
        icon_selector_form = VelgIkon()

        # Open the form as a modal dialog using alert()
        # Execution pauses here until the alert is closed
        selected_icon = alert(
            content=icon_selector_form,
            title="Velg Ikon",
            large=True,       # Optional: Adjust size as needed
            buttons=[]        # No default buttons, we close via events
        )

        # Code resumes here after VelgIkon closes

        # Check if the user selected an icon (didn't cancel)
        if selected_icon is not None:
            # Store the selected Media object
            self.selected_ikon_media = selected_icon
            # Update the preview image
            self.ikon_preview.source = self.selected_ikon_media
            print(f"Icon selected: {self.selected_ikon_media.name if self.selected_ikon_media else 'None'}")
        else:
            print("Icon selection cancelled.")
            # Optionally, you could set the icon back to None if cancelled
            # self.selected_ikon_media = None
            # self.ikon_preview.source = None

    def lagre_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        # Use the icon Media object stored in self.selected_ikon_media
        ikon = self.selected_ikon_media
        beskrivelse = self.beskrivelse.text

        print(f"Saving: Poeng={poeng}, Aktivitet='{aktivitet}', Ikon='{ikon.name if ikon else None}', Beskrivelse='{beskrivelse}'")

        # If PoengVelger was opened with a callback, call it now
        if self.callback:
            self.callback(poeng, aktivitet, ikon, beskrivelse)

        # Navigate back or close the form appropriately
        # If PoengVelger is a main form, navigate elsewhere:
        open_form('Loggbok') # Change 'Loggbok' if needed

        # If PoengVelger was opened via alert(), use this instead:
        # self.raise_event('x_close_alert', value=True) # Or return collected data

 