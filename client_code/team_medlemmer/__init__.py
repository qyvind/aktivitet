from ._anvil_designer import team_medlemmerTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class team_medlemmer(team_medlemmerTemplate):
  def __init__(self, teamnavn="", **properties):  # teamnavn hentes som en parameter
    self.init_components(**properties)

    # print(f"📢 Åpner team_medlemmer med teamnavn: {teamnavn}")  # Debugging

    # Kall serverfunksjonen med riktig teamnavn
    team_medl = anvil.server.call('hent_teammedlemmer', teamnavn)
    #print(team_medl)
    self.team_label.text = teamnavn
    # Sett inn data i et Repeating Panel hvis du har et
    self.team_medl_repeating_panel.items = [{"navn": member["navn"], "poeng": member["poeng"]} for member in team_medl]

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Loggbok')
    
