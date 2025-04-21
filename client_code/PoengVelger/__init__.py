from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# Make sure the import path is correct for your project structure
from ..VelgIkon import VelgIkon
from ..Utils import Utils

class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None,skritt=None, callback=None, **properties):
        self.init_components(**properties)
        self.callback = callback
        skrittf= Utils.hent_skritt_first()
        print('skritt_first',skrittf)
        if skrittf:
          print('skritt',skrittf )
          self.trening_panel_1.visible = False
          self.trening_panel_2.visible = False
          self.skritt_panel_1.visible = True
          self.skritt_panel_2.visible = True
        else:
          self.trening_panel_1.visible = True
          self.trening_panel_2.visible = True
          self.skritt_panel_1.visible = False
          self.skritt_panel_2.visible = False

      
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
        self.poeng_drop.items = [ ("En halv time", 1), ("En time", 2), ("Halvannen time eller mer", 3)]
        if valgt_poeng == 0:
          valgt_poeng = 1
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        #self.antall_skritt.text = skritt.text
        

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
            self.velg_aktivitet_label.text = selected_data.get('path')

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

    def lagre_trening_button_click(self, **event_args):
        poeng = self.poeng_drop.selected_value
        aktivitet = self.selected_ikon_path
        
        # Bruk de lagrede verdiene
        ikon_media = self.selected_ikon_media
        ikon_path = self.selected_ikon_path # Du har nå path her!
        beskrivelse = self.beskrivelse.text

        # Gjør noe med ikon_path hvis du trenger det her,
        # f.eks. lagre det i en annen tabell sammen med resten av dataen.
        #print(f"Lagrer med ikon path: {ikon_path}")


        # Hvis PoengVelger ble åpnet med en callback, kall den nå
        # Viktig: Hvis callback-funksjonen skal motta path, må signaturen oppdateres!
        if self.callback:
            # Du må bestemme om callback trenger path
            # Alternativ 1: Uten path (som før)
            # self.callback(poeng, aktivitet, ikon_media, beskrivelse)
            # Alternativ 2: Med path (krever endring der callback er definert)
             skritt=0
             self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path,skritt)
        anvil.server.call('sett_skritt_first',False)
        open_form('Loggbok')

    def lagre_skritt_click(self, **event_args):
        skritt_rad = app_tables.files.get(path = "Skritt")
        #if not skritt_rad or not skritt_rad['file']:
        #  alert("Fant ikke ikon for skritt – kontakt admin")
        #  return
        #tekst = self.antall_skritt.text
        #antall = 0
        #if tekst and tekst.isdigit():
        #    antall = int(tekst)
        #    
        #else:
        #    #alert("Du må skrive inn et gyldig tall for skritt.")
        poeng=1
     
        aktivitet = "Skritt"
        
        # Bruk de lagrede verdiene
        ikon_media = skritt_rad['file']
        ikon_path = aktivitet
        beskrivelse = self.beskrivelse.text


        #skritt = antall
        if self.callback:

             self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path)
        anvil.server.call('sett_skritt_first',True)
        open_form('Loggbok')

    def bytt_til_trening_click(self, **event_args):
      self.trening_panel_1.visible = True
      self.trening_panel_2.visible = True
      self.skritt_panel_1.visible = False
      self.skritt_panel_2.visible = False

    def nytt_til_skritt_button_click(self, **event_args):
      self.trening_panel_1.visible = False
      self.trening_panel_2.visible = False
      self.skritt_panel_1.visible = True
      self.skritt_panel_2.visible = True




  



 
