from ._anvil_designer import minsideTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Utils import Utils
from .. import Globals


class minside(minsideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.fyll_minside()

  def fyll_minside(self, **properties): 
    user = Globals.bruker
    print(user)
    deltagerdata= Utils.hent_brukernavn()
    framo_selskap_list = [row['navn'] for row in app_tables.framo_selskap.search() if row['navn'] ]
    self.framo_selskap_drop.items = [("", "")] + [(navn, navn) for navn in framo_selskap_list]


    
    
    self.poeng.text = deltagerdata['poeng']
    self.bonus.text = deltagerdata['bonus']
    self.longest_streak.text = deltagerdata['longest_streak']
    self.score.text = deltagerdata['score']
    self.liga_navn.text = deltagerdata['liga_navn']
    antall_deltagere = len(app_tables.userinfo.search())
    self.plassering.text = f"{deltagerdata['plassering']}/{antall_deltagere}"    
    antall_teams =  len(app_tables.team.search())
    self.team_plassering.text = f"{deltagerdata['team_plassering']}/{antall_teams}"
    self.plassering_i_team.text = f"{deltagerdata['plassering_i_team']}/{deltagerdata['team_members']}"
    self.team_score.text = deltagerdata['team_score']
    self.team.text = deltagerdata['team']
    self.framo_selskap_drop.selected_value = deltagerdata['framo_selskap']
    if self.team.text == "" :
      self.team_card.visible=False 
    else:
      self.team_card.visible = True

    liganavn=self.liga_navn.text
    if liganavn == "Diamant":
      source = "_/theme/liga_images/diamant.png"              
    elif liganavn == "Obsidian":
      source = "_/theme/liga_images/obsidian.png"              
    elif liganavn == "Perle":
      source = "_/theme/liga_images/perle.png"
    elif liganavn == "Safir":
      source = "_/theme/liga_images/safir.png"
    elif liganavn == "Sølv":
      source = "_/theme/liga_images/solv.png"
    elif liganavn == "Ametyst":
      source = "_/theme/liga_images/ametyst.png"  
    elif liganavn == "Bronse":
      source = "_/theme/liga_images/bronse.png"
    elif liganavn == "Gull":
      source = "_/theme/liga_images/gull.png"
    elif liganavn == "Rubin":
      source = "_/theme/liga_images/rubin.png"
    elif liganavn == "Smaragd":
      source = "_/theme/liga_images/smaragd.png"
    self.liga_image.source = source
    self.liga_image.tooltip = f"Liga: {liganavn}"

    self.opprykk_symbol.text = deltagerdata['opprykk_symbol']
    status = deltagerdata['opprykk_status']
    if status == "up":
      self.opprykk_beskrivelse.text = "Du ligger an til å rykke opp en liga etter denne uken. Det vil gi deg ekstra bonuspoeng"
    elif status == "down":
      self.opprykk_beskrivelse.text = "Du risikerer å rykke ned en liga etter denne uken. Kanskje du kan gjøre noe med det?"
    elif status == "same":
      self.opprykk_beskrivelse.text = "Du ser ut til å bli værende i denne ligaen etter denne uken."

    
    navn=deltagerdata['navn']
    mitt_team=deltagerdata['team']
    #plassering = deltagerdata['plassering']
    self.user_email_label.text = user['email']
    self.navn_textbox.text = navn
    if deltagerdata['lock']:
      self.locked.icon = 'fa:lock'
      self.team_medlem.text = mitt_team
      self.team_medlem.visible = True
      self.team_drop_down.visible = False
      self.lag_team_panel.visible = False 
    else:
      self.locked.icon = 'fa:unlock'
      self.lag_team_panel.visible = True 
      team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]
      self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]
      
      self.team_drop_down.selected_value = mitt_team
      self.team_medlem.visible = False
      self.team_drop_down.visible = True
    team_medl = Utils.hent_teammedlemmer(mitt_team)
    
    self.team_medl_repeating_panel.items = [{"navn": member["navn"], "poeng": member["poeng"],"bonus": member["bonus"], "lengste_streak":member["lengste_streak"],"score":member["score"],"userrecord":member["userrecord"]} for member in team_medl]
    self.vis_tildelte_badges(Globals.bruker)  
    

  def angre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Loggbok')

  def lagre_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('oppdater_brukernavn_og_team',self.navn_textbox.text,self.team_drop_down.selected_value)
    open_form('Loggbok')

  def nytt_team_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.nytt_team.text = anvil.server.call('opprett_nytt_team',self.nytt_team.text)
    team_list = [row['team'] for row in app_tables.team.search() if row['team'] and not row['lock']]
    self.team_drop_down.items = [("", "")] + [(team, team) for team in team_list]

  def locked_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.locked.icon != 'fa:lock':
      resultat = anvil.server.call('laas_eget_team')
      alert(resultat)
      self.fyll_minside()
    

  def badge_1_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_1.tooltip)
  def badge_2_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_2.tooltip)
  def badge_3_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_3.tooltip)
  def badge_4_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_4.tooltip)
  def badge_5_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_5.tooltip)
  def badge_6_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_6.tooltip)
  def badge_7_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_7.tooltip)
  def badge_8_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_8.tooltip)
  def badge_9_mouse_down(self, x, y, button, keys, **event_args):
    alert(self.badge_9.tooltip)


  def image_mouse_enter(self, x, y, **event_args):
    anvil.js.window.document.body.style.cursor = 'pointer'

  def image_mouse_leave(self, x, y, **event_args):
    anvil.js.window.document.body.style.cursor = 'default'

  def vis_tildelte_badges(self, bruker):
      #print("▶️ Viser badges for:", bruker['email'])
  
      user_badger = app_tables.user_badges.search(user=bruker)
      for rad in user_badger:
          badge = rad['badge']
          badge_id = badge['id']
          #print(f" - Har badge {badge_id}: {badge['name']}")
  
          badge_komponent = getattr(self, f"badge_{badge_id}", None)
          if badge_komponent:
              self.badge_flow_panel.visible = True
              badge_komponent.visible = True

  def framo_selskap_drop_change(self, **event_args):
    alert(anvil.server.call('sett_framo_selskap_for_user',self.framo_selskap_drop.selected_value,Globals.bruker))