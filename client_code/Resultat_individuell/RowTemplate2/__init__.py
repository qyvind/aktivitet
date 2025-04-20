from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables




class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.Deltager_label.text = self.item['deltager']
    poeng = self.item['poeng']
    self.team_label.text = self.item['team']
    self.email.text = self.item['email']
    streak = self.item['longest_streak']    
    self.score.text = self.item['score']
    bonus = self.item['bonus']
    self.score.tooltip = f"((Poeng: {poeng} + Bonus: {bonus}) * 100) + Streak: {streak}"
    #self.vis_tildelte_badges(self.item['email'])
    
    

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    email = self.email.text
    try:
        bruker_rad = anvil.server.call("hent_user_fra_email", email)
        open_form("BrukerLoggbok", enuser=bruker_rad)
    except Exception as e:
        alert(f"Feil: {e}")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    coaching = anvil.server.call('lag_status_for_bruker')
    print(coaching)

  # def vis_tildelte_badges(self, bruker):
  #     print("▶️ Viser badges for:", self.item['deltager'])
  
  #     user_badger = app_tables.user_badges.search(user = bruker)
  #     for rad in user_badger:
  #         badge = rad['badge']
  #         badge_id = badge['id']
  #         print(f" - Har badge {badge_id}: {badge['name']}")
  
  #         badge_komponent = getattr(self, f"badge_{badge_id}", None)
  #         if badge_komponent:
  #             self.badge_flow_panel.visible = True
  #             badge_komponent.visible = True