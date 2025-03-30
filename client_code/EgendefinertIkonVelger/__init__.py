from ._anvil_designer import EgendefinertIkonVelgerTemplate
from anvil import *
from anvil.media import *

class EgendefinertIkonVelger(EgendefinertIkonVelgerTemplate):
  def __init__(self, callback=None, **properties):
    self.init_components(**properties)
    self.callback = callback

    # Liste med ikondata (oppdater med filnavnene du har lastet opp)
    self.ikoner = [
      {"navn": "crossfit", "dumbell-weight": app_files.fotball_png},
      {"navn": "Frisbee", "fil": app_files.frisbee_png},
      {"navn": "Orientering", "fil": app_files.map-hiking_png},
      {"navn": "Klatring", "fil": app_files.person-climbing_png},
      {"navn": "Yoga", "fil": app_files.yoga_png},
      {"navn": "Svømming", "fil": app_files.swimming_png},
      {"navn": "Løp", "fil": app_files.running_png},
      {"navn": "8000 skritt", "fil": app_files.walking_png},
    ]

    self.vis_ikoner()

  def vis_ikoner(self):
    for ikon in self.ikoner:
      img = Image(source=ikon["fil"], width=60, height=60)
      lbl = Label(text=ikon["navn"], align="center")
      col = ColumnPanel()
      col.add_component(img)
      col.add_component(lbl)
      img.tag.valgt_source = ikon["fil"]
      img.set_event_handler("click", self.ikon_valgt)
      self.ikon_flowpanel.add_component(col)

  def ikon_valgt(self, sender, **event_args):
    if self.callback:
      self.callback(sender.tag.valgt_source)  # Send tilbake bilde-referansen
    self.raise_event("x-close")
