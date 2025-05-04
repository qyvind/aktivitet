from ._anvil_designer import BrukerLoggbokTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import Globals
from anvil_extras.animation import Effect, Transition
import time


class BrukerLoggbok(BrukerLoggbokTemplate):
    def __init__(self, enuser=None, **properties):
        self.enuser = enuser  # Brukeren vi skal vise logg for
        self.init_components(**properties)

        Globals.week_offset = 0
        self.initier_uke(Globals.week_offset)
        self.sjekk_bruker()
        
        self.vis_tildelte_badges(enuser)

    def initier_uke(self, week_offset):
        self.get_week_info(week_offset)
        self.uke_label.text = self.get_week_range(week_offset)
        week_activities = self.get_activities_for_week()
        self.fyll_skjermen(week_activities)

    def get_week_info(self, week_offset):
        today = datetime.today()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday) + timedelta(weeks=week_offset)
        sunday = monday + timedelta(days=6)
        week_number = monday.isocalendar()[1]
        return {
            "week_number": week_number,
            "monday": monday.strftime("%Y-%m-%d"),
            "sunday": sunday.strftime("%Y-%m-%d"),
            "monday_date": monday.date(),
            "sunday_date": sunday.date()
        }

    def get_week_range(self, week_offset):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        monday_date = start_of_week + timedelta(weeks=week_offset)
        sunday_date = monday_date + timedelta(days=6)
        month_names = {
            1: "jan", 2: "feb", 3: "mars", 4: "april", 5: "mai", 6: "juni",
            7: "juli", 8: "aug", 9: "sep", 10: "okt", 11: "nov", 12: "des"
        }
        if monday_date.month == sunday_date.month:
            return f"{monday_date.day} - {sunday_date.day} {month_names[monday_date.month]}"
        else:
            return f"{monday_date.day} {month_names[monday_date.month]} - {sunday_date.day} {month_names[sunday_date.month]}"

    def get_activities_for_week(self):
        user = self.enuser or anvil.users.get_user()
        if not user:
            return {day: [] for day in range(7)}
        week_info = self.get_week_info(Globals.week_offset)
        start = week_info['monday_date']
        end = week_info['sunday_date']
        activities = app_tables.aktivitet.search(
            tables.order_by('dato'),
            deltager=user,
            dato=q.between(start, end + timedelta(days=1))
        )
        week_activities = {day: [] for day in range(7)}
        for act in activities:
            day = act['dato'].weekday()
            week_activities[day].append({
                'aktivitet': act['aktivitet'],
                'poeng': act['poeng'],
                'ikon': act['ikon'],
                'beskrivelse': act['beskrivelse'],
            })
        return week_activities

    def fyll_skjermen(self, week_activities):
        base_dato = self.get_week_info(Globals.week_offset)['monday_date']
        komponenter = [
            (self.man_button, self.man_column_panel, self.man_akt_label, week_activities[0], base_dato, self.man_ikon),
            (self.tir_button, self.tir_column_panel, self.tir_akt_label, week_activities[1], base_dato + timedelta(days=1), self.tir_ikon),
            (self.ons_button, self.ons_column_panel, self.ons_akt_label, week_activities[2], base_dato + timedelta(days=2), self.ons_ikon),
            (self.tor_button, self.tor_column_panel, self.tor_akt_label, week_activities[3], base_dato + timedelta(days=3), self.tor_ikon),
            (self.fre_button, self.fre_column_panel, self.fre_akt_label, week_activities[4], base_dato + timedelta(days=4), self.fre_ikon),
            (self.lor_button, self.lor_column_panel, self.lor_akt_label, week_activities[5], base_dato + timedelta(days=5), self.lor_ikon),
            (self.son_button, self.son_column_panel, self.son_akt_label, week_activities[6], base_dato + timedelta(days=6), self.son_ikon),
        ]

        today_date = datetime.today().date()

        for knapp, panel, label, akt_data, dato, ikon_komponent in komponenter:
            if akt_data:
                poeng = str(akt_data[0]['poeng'])
                aktivitet = akt_data[0]['aktivitet']
                ikon = akt_data[0]['ikon']
                tooltip = akt_data[0]['beskrivelse']
            else:
                poeng = "0"
                aktivitet = "Hviledag"
                ikon = None
                tooltip = ""

            knapp.text = poeng
            label.text = aktivitet
            ikon_komponent.source = ikon
            ikon_komponent.tooltip = tooltip

            fremtid = dato > today_date
            knapp.enabled = False  # 🔒 Deaktivert uansett hvem som vises

            panel.background = "#e0e0e0" if poeng == "0" else self.get_farge(poeng)

    def get_farge(self, poeng_verdi):
        farge_mapping = {
            "0": "#e0e0e0",
            "1": "#b2f2bb",
            "2": "#69db7c",
            "3": "#2b8a3e"
        }
        return farge_mapping.get(str(poeng_verdi), "#e0e0e0")


    def next_week_button_click(self, **event_args):
      #fixed_animation_height = 650 # Juster denne verdien etter behov
      #self.loggbok_card.height = fixed_animation_height
    
      slide_out = Transition(translateX=["0%", "-100%"])
      slide_in = Transition(translateX=["100%", "0%"])
      out_effect = Effect(slide_out, duration=400)
      in_effect = Effect(slide_in, duration=400)
      
      
      out_effect.animate(self.week_row_panel).wait()  # Vent til animasjonen er ferdig
      in_effect.animate(self.week_row_panel)
      
      
      
      Globals.week_offset +=1
      #self.lagre_week_offset()
      self.initier_uke(Globals.week_offset)

    def prev_week_button_click(self, **event_args):
      
      #fixed_animation_height = 650 # Juster denne verdien etter behov
      #self.loggbok_card.height = fixed_animation_height
    
      # Skjul nåværende uke med en glidende ut-effekt
      slide_out = Transition(translateX=["0%", "100%"])
      slide_in = Transition(translateX=["-100%", "0%"])
      out_effect = Effect(slide_out, duration=400)
      in_effect = Effect(slide_in, duration=400)
      
      
      out_effect.animate(self.week_row_panel).wait()  # Vent til animasjonen er ferdig
      in_effect.animate(self.week_row_panel)
      
      Globals.week_offset -= 1
      
      self.initier_uke(Globals.week_offset)


  
    # def next_week_button_click(self, **event_args):
    #     Globals.week_offset += 1
    #     self.initier_uke(Globals.week_offset)

    # def prev_week_button_click(self, **event_args):
    #     Globals.week_offset -= 1
    #     self.initier_uke(Globals.week_offset)

    def sjekk_bruker(self):
        if self.enuser:
            userinfo = app_tables.userinfo.get(user=self.enuser)
            if userinfo:
                self.deltager_label.text = userinfo['navn']
                self.team_label.text = userinfo['team']['team'] if userinfo['team'] else "Uten team"

                # # setter liga_ikon
                # if userinfo['liga_navn']:
                #   #liga_ikon = userinfo['liga_ikon']
                #   liga_navn = userinfo['liga_navn']

                # else:
                #     #liga_ikon = " "
                #     liga_navn = " "
              
            
                # if liga_navn == "Diamant":
                #   source = "_/theme/liga_images/diamant.png"              
                # elif liga_navn == "Obsidian":
                #   source = "_/theme/liga_images/obsidian.png"              
                # elif liga_navn == "Perle":
                #   source = "_/theme/liga_images/perle.png"
                # elif liga_navn == "Safir":
                #   source = "_/theme/liga_images/safir.png"
                # elif liga_navn == "Sølv":
                #   source = "_/theme/liga_images/solv.png"
                # elif liga_navn == "Ametyst":
                #   source = "_/theme/liga_images/ametyst.png"  
                # elif liga_navn == "Bronse":
                #   source = "_/theme/liga_images/bronse.png"
                # elif liga_navn == "Gull":
                #   source = "_/theme/liga_images/gull.png"
                # elif liga_navn == "Rubin":
                #   source = "_/theme/liga_images/rubin.png"
                # elif liga_navn == "Smaragd":
                #   source = "_/theme/liga_images/smaragd.png"
                #   self.liga_image.source = source
                # self.liga_image_copy.source = source
                # self.liga_image.tooltip = f"Liga: {liga_navn}"
                # self.liga_image_copy.tooltip = f"Liga: {liga_navn}"
                    

              
        else:
            user = anvil.users.get_user()
            if user:
                userinfo = app_tables.userinfo.get(user=user)
                if userinfo:
                    self.deltager_label.text = userinfo['navn']
                    self.team_label.text = userinfo['team']['team'] if userinfo['team'] else "Uten team"
                

    def logout_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form(('Resultat_individuell'))

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