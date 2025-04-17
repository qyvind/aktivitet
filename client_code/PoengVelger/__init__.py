from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# Make sure the import path is correct for your project structure
from ..VelgIkon import VelgIkon

class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None, skritt = None, callback=None, **properties):
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
        print('poengvelger ',skritt)
        self.ukedag_label.text = ukedag
        self.poeng_drop.items = [("0 poeng", 0), ("1 poeng", 1), ("2 poeng", 2), ("3 poeng", 3)]
        self.poeng_drop.selected_value = valgt_poeng
        self.skritt.text = skritt
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

            #print(f"Ikon valgt: Media={self.selected_ikon_media.name if self.selected_ikon_media else 'None'}, Pent Navn (fra path)={self.selected_ikon_path}")

            # --- HER ER DEN FORENKLEDE LOGIKKEN ---
            # Sjekk om aktivitet_box er tom OG vi faktisk har fått et pent navn
            if not self.aktivitet_box.text and self.selected_ikon_path:
                # Sett aktivitet_box.text direkte til det pene navnet fra 'path'-feltet
                self.aktivitet_box.text = self.selected_ikon_path
            # --- SLUTT PÅ FORENKLET LOGIKK ---

        else:
            print("Valg av ikon avbrutt.")

    def OK_click(self, **event_args):
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        skritt = self.skritt.text
        beskrivelse = self.beskrivelse.text
        ikon_path = self.selected_ikon_path
        ikon_media = self.selected_ikon_media  # <-- original verdi
    
        try:
            antall_skritt = int(skritt or 0)
        except ValueError:
            antall_skritt = 0
    
        # 🔁 Automatisk ikon hvis kun skritt
        
        if antall_skritt > 0 and not ikon_media:
          
            ikon_media = self.walking.source
            self.selected_ikon_media = ikon_media  # <-- 🔥 viktig!
            self.ikon_preview.source = ikon_media  # <-- vis i forhåndsvisning
            self.aktivitet_box.text = f"{antall_skritt} Skritt"
            self.poeng_drop.selected_value = 1
        poeng = self.poeng_drop.selected_value
        aktivitet = self.aktivitet_box.text
        beskrivelse = self.beskrivelse.text
        
    
        if self.callback:
            self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path, skritt)
    
        open_form("Loggbok")



          



    def lagre_skritt_button_click(self, **event_args):
      try:
          antall = int(self.skritt.text)
          if antall > 0:
              self.aktivitet_box.text = f"{antall} Skritt"
              self.poeng_drop.selected_value = 1
              loggbok = get_open_form()
              if hasattr(loggbok, "skritt") and loggbok.skritt.source:
                self.selected_ikon_media = loggbok.skritt.source
                self.ikon_preview.source = self.selected_ikon_media
              
        
        
          else:
              #alert("Vennligst skriv et positivt tall.")
              pass
      except (ValueError, TypeError):
          alert("Skriv inn et gyldig tall.")


  

