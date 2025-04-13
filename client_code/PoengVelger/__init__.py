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
        self.init_components(**properties)
        self.callback = callback

        # --- MODIFISERT DEL START ---
        # Lagre både Media-objektet og path-strengen
        self.selected_ikon_media = None # Initialiser som None
        self.selected_ikon_path = None  # Initialiser som None

        # Hvis et ikon ble sendt inn ved initialisering, anta at det KUN er Media-objektet
        # Du *kan* trenge å hente path separat hvis du initialiserer med et ikon her
        # ELLER endre hvordan du kaller PoengVelger for å sende inn path også.
        # For enkelhets skyld antar vi her at initialisering med 'ikon' ikke trenger path med en gang.
        if ikon:
             self.selected_ikon_media = ikon
             # Hvis du trenger path her også, må du ha en måte å finne den på basert på 'ikon'
             # f.eks. et oppslag i databasen.
             # self.selected_ikon_path = hent_path_for_media(ikon) # (Pseudokode)

        # --- MODIFISERT DEL SLUTT ---

        self.ukedag_label.text = ukedag
        self.poeng_drop.items = [("0 poeng", 0), ("1 poeng", 1), ("2 poeng", 2), ("3 poeng", 3)]
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        if self.aktivitet_box.text == "Hviledag":
            self.aktivitet_box.text = ""
        self.beskrivelse.text = beskrivelse

        # Sett den initielle forhåndsvisningen
        self.ikon_preview.source = self.selected_ikon_media


    def ikon_preview_click(self, **event_args):
        """This method is called when the ikon_preview Image is clicked."""
        icon_selector_form = VelgIkon()
        selected_data = alert(
            content=icon_selector_form,
            title="Velg Ikon",
            large=True,
            buttons=[]
        )

        if selected_data is not None:
            self.selected_ikon_media = selected_data.get('media')
            self.selected_ikon_path = selected_data.get('path') # Dette er nå det pene navnet

            self.ikon_preview.source = self.selected_ikon_media

            print(f"Ikon valgt: Media={self.selected_ikon_media.name if self.selected_ikon_media else 'None'}, Pent Navn (fra path)={self.selected_ikon_path}")

            # --- HER ER DEN FORENKLEDE LOGIKKEN ---
            # Sjekk om aktivitet_box er tom OG vi faktisk har fått et pent navn
            if not self.aktivitet_box.text and self.selected_ikon_path:
                # Sett aktivitet_box.text direkte til det pene navnet fra 'path'-feltet
                self.aktivitet_box.text = self.selected_ikon_path
            # --- SLUTT PÅ FORENKLET LOGIKK ---

        else:
            print("Valg av ikon avbrutt.")

    def lagre_button_click(self, **event_args):
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        # Bruk de lagrede verdiene
        ikon_media = self.selected_ikon_media
        ikon_path = self.selected_ikon_path # Du har nå path her!
        beskrivelse = self.beskrivelse.text

        # Gjør noe med ikon_path hvis du trenger det her,
        # f.eks. lagre det i en annen tabell sammen med resten av dataen.
        print(f"Lagrer med ikon path: {ikon_path}")


        # Hvis PoengVelger ble åpnet med en callback, kall den nå
        # Viktig: Hvis callback-funksjonen skal motta path, må signaturen oppdateres!
        if self.callback:
            # Du må bestemme om callback trenger path
            # Alternativ 1: Uten path (som før)
            # self.callback(poeng, aktivitet, ikon_media, beskrivelse)
            # Alternativ 2: Med path (krever endring der callback er definert)
             self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path)

        open_form('Loggbok')
