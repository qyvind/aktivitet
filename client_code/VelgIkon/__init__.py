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
ItemTemplate1 = anvil.imports.import_from('ItemTemplate1')


class VelgIkon(VelgIkonTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    ikon_rader = app_tables.files.search()
    ikoner = [{"file": rad['file']} for rad in ikon_rader if rad['file']]
    
    # Legg til valget "Ingen ikon"
    ikoner.insert(0, {"file": None})
    
    self.ikon_grid.clear()
    
    num_cols = 3
    for i, ikon in enumerate(ikoner):
      rad = i // num_cols
      col = i % num_cols
      
      komponent = ItemTemplate1(item=ikon)
      self.ikon_grid.add_component(komponent, row=rad, col=col)
