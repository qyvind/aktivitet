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


class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None, callback=None, **properties):
        self.init_components(**properties)
        self.ukedag_label.text = ukedag
        self.callback = callback

        self.poeng_drop.items = [
            ("0 poeng", 0),
            ("1 poeng", 1),
            ("2 poeng", 2),
            ("3 poeng", 3)
        ]
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        if self.aktivitet_box.text == "Hviledag":
            self.aktivitet_box.text= ""
        self.beskrivelse.text = beskrivelse

        # Hent ikonene fra Files-tabellen (Media-objekter)
        ikon_rader = app_tables.files.search()
        ikoner = [(rad['path'], rad['file']) for rad in ikon_rader if rad['file']]
        
        # Legg til "Ingen ikon"-valg
        ikoner.insert(0, ("Ingen ikon", None))
        
        self.ikon_dropdown.items = ikoner
        self.ikon_dropdown.include_placeholder = False

        # Forhåndsvis valgt ikon
        self.valgt_ikon = ikon
        for label, media in self.ikon_dropdown.items:
            if ikon and media and hasattr(ikon, "name") and ikon.name == media.name:
                self.ikon_dropdown.selected_value = media
                self.ikon_preview.source = media
                break

        else:
            self.ikon_dropdown.selected_value = None
            self.ikon_preview.source = None

    def ikon_dropdown_change(self, **event_args):
        valgt = self.ikon_dropdown.selected_value
        if valgt:
            self.ikon_preview.source = valgt
        else:
            self.ikon_preview.source = None
    
    def lagre_button_click(self, **event_args):
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        ikon = self.ikon_dropdown.selected_value  # Dette er nå et Media-objekt eller None
        beskrivelse = self.beskrivelse.text

        if self.callback:
            self.callback(poeng, aktivitet, ikon, beskrivelse)

        open_form('Loggbok')  # Gå tilbake til hovedform

    def ikon_preview_mouse_down(self, x, y, button, keys, **event_args):
        """This method is called when a mouse button is pressed on this component"""
        def set_ikon_preview(image):
            self.ikon_preview.source = image
        
        open_form('VelgIkon', callback=set_ikon_preview)