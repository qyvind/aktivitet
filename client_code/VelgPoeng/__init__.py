from ._anvil_designer import VelgPoengTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class VelgPoeng(VelgPoengTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.poeng_drop.items = [("Kortere enn en halv time", 0), ("En halv time", 1), ("En time", 2), ("Halvannen time eller mer", 3)]
    self.poeng_drop.selected_value = 0
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

    self.ikon_repeating_panel.add_event_handler('x-icon-click', self.icon_selected)

 

    
  def registrer_trening_click(self, **event_args):
    self.skritt_panel_1.visible = False
    self.skritt_panel_2.visible = False 
    self.trening_panel_1.visible = True
    self.trening_panel_2.visible = True 

  def registrer_skritt_click(self, **event_args):
    self.skritt_panel_1.visible = True
    self.skritt_panel_2.visible = True
    self.trening_panel_1.visible = False
    self.trening_panel_2.visible = False

  def icon_selected(self, icon_data, **event_args):
      self.icon_preview.source = icon_data['media']
      self.valgt_ikon_media = icon_data['media']
      self.valgt_ikon_path = icon_data['path']
  
      # Fjern ramme fra tidligere valg
      if hasattr(self, 'valgt_bilde') and self.valgt_bilde:
          self.valgt_bilde.border = None
  
      # Marker det nye bildet
      clicked_image = event_args.get('clicked_image')
      if clicked_image:
          clicked_image.border = "3px solid #2196F3"
          self.valgt_bilde = clicked_image

  def lagre_trening_click(self, **event_args):
    aktivitet = self.valgt_ikon_path
    beskrivelse = self.beskrivelse.text  # Hvis du har en sånn
    print("✅ Sender data tilbake til Loggbok via x-close-alert")
    print("🔁 raise_event med:")
    print("  poeng:", self.poeng_drop.selected_value)
    print("  aktivitet:", aktivitet)
    print("  ikon:", self.valgt_ikon_media)
    print("  path:", self.valgt_ikon_path)
    print("  beskrivelse:", beskrivelse)
    self.raise_event('x-close-alert', value={
        'poeng': self.poeng_drop.selected_value,
        'aktivitet': aktivitet,
        'ikon': self.valgt_ikon_media,
        'path': self.valgt_ikon_path,
        'beskrivelse': beskrivelse
    })
    


