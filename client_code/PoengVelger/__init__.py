from ._anvil_designer import PoengVelgerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# Make sure the import path is correct for your project structure
from ..VelgIkon import VelgIkon
from ..Utils import Utils
import anvil.js
from .. import Globals

class PoengVelger(PoengVelgerTemplate):
    def __init__(self, valgt_poeng=1, aktivitet="", ukedag="", ikon=None, beskrivelse=None,skritt=None, callback=None, **properties):
        self.init_components(**properties)
        self.callback = callback
        #skrittf= Globals.skrittf
        #self.skrittf_box.checked = skrittf
        #print('skritt_first',skrittf)
        if Globals.skrittf:
        #  print('skritt',skrittf )
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


        if ikon:
             self.selected_ikon_media = ikon


        self.ukedag_label.text = ukedag
        self.poeng_drop.items = [ ("Hviledag",0),("En halv time", 1), ("En time", 2), ("Halvannen time eller mer", 3)]
        if valgt_poeng == 0:
          valgt_poeng = 1
        self.poeng_drop.selected_value = valgt_poeng
        self.aktivitet_box.text = aktivitet
        #self.antall_skritt.text = skritt.text

        self.skritt_drop.items = [ ("8000 skritt", 1), ("16000 skritt", 2), ("24000 skritt eller mer", 3)]
        self.skritt_drop.selected_value = valgt_poeng

        self.beskrivelse.text = beskrivelse
        self.ikon_preview.source = "_/theme/treninger.png"

        # Sett den initielle forhåndsvisningen
        self.ikon_preview.source = self.selected_ikon_media
        if ikon:
            self.selected_ikon_media = ikon
            self.ikon_preview.source = ikon
            self.velg_aktivitet_label.text = aktivitet
            
            
        else:
            self.selected_ikon_media = None
            self.ikon_preview.source = "_/theme/treninger.png"

        #self.selected_ikon_path = None


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
            if self.selected_ikon_path == "Hviledag":
              self.velg_lengde_panel.visible = False
            else:
              self.velg_lengde_panel.visible = True

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
        
        aktivitet = self.selected_ikon_path
        
        # Bruk de lagrede verdiene
        ikon_media = self.selected_ikon_media
        ikon_path = self.selected_ikon_path # Du har nå path her!
        poeng = self.poeng_drop.selected_value
        beskrivelse = self.beskrivelse.text

        if self.callback:

             skritt=0
             self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path,skritt)
        if Globals.skrittf:
          Globals.skrittf = False
        open_form('Loggbok')

    def lagre_skritt_click(self, **event_args):
        skritt_rad = app_tables.files.get(path = "Skritt")
        
        poeng=self.skritt_drop.selected_value
     
        aktivitet = "Skritt"
        
        # Bruk de lagrede verdiene
        ikon_media = skritt_rad['file']
        ikon_path = aktivitet
        beskrivelse = self.beskrivelse.text


        #skritt = antall
        if self.callback:

             self.callback(poeng, aktivitet, ikon_media, beskrivelse, ikon_path)
        
        if not Globals.skrittf:
          Globals.skrittf = True
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

    def ikon_preview_mouse_enter(self, x, y, **event_args):
      anvil.js.window.document.body.style.cursor = 'pointer'

    def ikon_preview_mouse_leave(self, x, y, **event_args):
      anvil.js.window.document.body.style.cursor = 'default'

    def angre_button_click(self, **event_args):
      open_form('Loggbok')





  



 
