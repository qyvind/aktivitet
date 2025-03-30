from ._anvil_designer import EgendefinertIkonVelgerTemplate
from anvil import *
from anvil.media import *

class EgendefinertIkonVelger(EgendefinertIkonVelgerTemplate):
  def __init__(self, callback=None, **properties):
    self.init_components(**properties)
    self.callback = callback

    # Liste med ikondata (oppdater med filnavnene du har lastet opp)
    self.ikoner = [
      {"navn": "Fotball", "fil": app_files.fotball_png},
      {"navn": "Basketball", "fil": app_files.basketball_png},
      {"navn": "Løping", "fil": app_files.running_png},
      {"navn": "Sykling", "fil": app_files.cycling_png},
      {"navn": "Yoga", "fil": app_files.yoga_png},
      {"navn": "Svømming", "fil": app_files.swimming_png},
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
