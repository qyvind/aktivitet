from ._anvil_designer import LoggbokTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class Loggbok(LoggbokTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.week_offset_label.text = 0
        self.initier_uke(self.week_offset_label.text)

        user = anvil.users.get_user()
        if user:
            # Brukeren er logget inn
            self.login_card.visible = False
            self.loggbok_card.visible = True
        else:
            self.loggbok_card.visible = False
            self.login_card.visible = True



    def initier_uke(self,week_offset):
        self.get_week_info(week_offset)
        self.uke_label.text = self.get_week_range(week_offset)
        week_activities = self.get_activities_for_week()
        self.fyll_skjermen(week_activities)
        
      
    def update_button_state(self, button, label, dato):
        """Oppdaterer knappens tekst og farge basert på nåværende tilstand"""
        states = {
            "0": ("1", "RED"),
            "1": ("2", "ORANGE"),
            "2": ("3", "GREEN"),
            "3": ("0", "BLACK"),
        }

        if button.text in states:
            button.text, button.foreground = states[button.text]
        else:
            print("button not in states")
              # Initialiser text_box med en default-verdi
        text_box = type('Dummy', (object,), {"text": ""})()  # Oppretter et objekt med et tomt text-attributt
        if button.text == "1":
            """Viser en popup for å spørre om tekst og oppdaterer en label"""
            text_box = TextBox(placeholder="Skriv her...")
    
            result = anvil.alert(
                content=text_box,
                title="Skriv inn type aktivitet",
                buttons=["OK", "Avbryt"]
            )
    
            if result == "OK":  # Hvis brukeren trykket "OK"
                label.text = text_box.text  # Hent tekst fra TextBox og sett den i riktig label
                # Lagre aktiviteten med riktig dato
        
        self.lagre_aktivitet(dato, text_box.text, int(button.text))
    
        # if button.text in states:
        #     button.text, button.foreground = states[button.text]
        # else:
        #     print("button not in states")

    def man_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        mandag_dato = week_info['monday_date']
        self.update_button_state(self.man_button, self.man_akt_label, mandag_dato)

    def tir_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        tirsdag_dato = week_info['monday_date'] + timedelta(days=1)
        self.update_button_state(self.tir_button, self.tir_akt_label, tirsdag_dato)

    def ons_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        onsdag_dato = week_info['monday_date'] + timedelta(days=2)
        self.update_button_state(self.ons_button, self.ons_akt_label, onsdag_dato)
    
    def tor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        torsdag_dato = week_info['monday_date'] + timedelta(days=3)
        self.update_button_state(self.tor_button, self.tor_akt_label, torsdag_dato)
    
    def fre_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        fredag_dato = week_info['monday_date'] + timedelta(days=4)
        self.update_button_state(self.fre_button, self.fre_akt_label, fredag_dato)
    
    def lor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        lordag_dato = week_info['monday_date'] + timedelta(days=5)
        self.update_button_state(self.lor_button, self.lor_akt_label, lordag_dato)
      
    def son_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        sondag_dato = week_info['monday_date'] + timedelta(days=6)
        self.update_button_state(self.son_button, self.son_akt_label, sondag_dato)

    def login_click(self, **event_args):
        """This method is called when the button is clicked"""
        user = anvil.users.login_with_form(allow_remembered=30, allow_cancel=True)
        if user:
            self.deltager_label.text = user['email']
            self.loggbok_card.visible = True
            self.login_card.visible = False

    def logout_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.users.logout()
        self.login_card.visible = True
        self.loggbok_card.visible = False


    def get_week_info(self, week_offset):
        today = datetime.today()
    
        # Finn mandagen i denne uken (første dag i uken)
        days_since_monday = today.weekday()  # Mandag = 0, Søndag = 6
        monday = today - timedelta(days=days_since_monday)
    
        # Juster mandagen basert på week_offset
        monday += timedelta(weeks=week_offset)
    
        # Finn søndagen i denne uken (siste dag i uken)
        sunday = monday + timedelta(days=6)
    
        # Hent ukenummer basert på mandagen etter week_offset
        week_number = monday.isocalendar()[1]  # Ukenummer basert på den justerte mandagen
    
        return {
            "week_number": week_number,
            "monday": monday.strftime("%Y-%m-%d"),  # Mandag som string
            "sunday": sunday.strftime("%Y-%m-%d"),  # Søndag som string
            "monday_date": monday.date(),  # Mandag som date-objekt
            "sunday_date": sunday.date()   # Søndag som date-objekt
        }


    def get_week_range(self, week_offset):
      # Dagens dato
      today = datetime.today()
    
      # Finn mandagen i den nåværende uken
      start_of_week = today - timedelta(days=today.weekday())
    
      # Juster mandagen basert på week_offset
      monday_date = start_of_week + timedelta(weeks=week_offset)
    
      # Finn søndagen i samme uke
      sunday_date = monday_date + timedelta(days=6)
    
      # Formater datoene
      month_names = {
          1: "jan", 2: "feb", 3: "mars", 4: "april", 5: "mai", 6: "juni",
          7: "juli", 8: "aug", 9: "sep", 10: "okt", 11: "nov", 12: "des"
      }
      result = f"{monday_date.day} - {sunday_date.day} {month_names[monday_date.month]}"
      return result

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.week_offset_label.text +=1
      self.initier_uke(self.week_offset_label.text)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.week_offset_label.text -=1
      self.initier_uke(self.week_offset_label.text)



    def get_activities_for_week(self):
        # Få den påloggede brukeren
        user = anvil.users.get_user()
        if not user:
            return {day: [] for day in range(7)}  # Returner en dictionary med alle dager
        
        # Få datoene for den aktive uken (mandag til søndag)
        week_info = self.get_week_info(self.week_offset_label.text)
        start_of_week = week_info['monday_date']  # Mandag som date-objekt
        end_of_week = week_info['sunday_date']  # Søndag som date-objekt
        
        try:
            # Hent aktivitetene kun for påloggede bruker innenfor ukens datoer
            activities = app_tables.aktivitet.search(
                tables.order_by('dato'),
                deltager=user,  # Filtrer på innlogget bruker
                dato=q.between(start_of_week, end_of_week + timedelta(days=1))  # Filtrer på datoer
            )
        except Exception as e:
            print(f"Error fetching activities: {e}")
            return {}
        
        # Organisere aktivitetene i en liste med 7 dager (0=Mandag, 6=Søndag)
        week_activities = {day: [] for day in range(7)}
        
        for activity in activities:
            activity_date = activity['dato']
            day_of_week = activity_date.weekday()  # Mandag = 0, Søndag = 6
            week_activities[day_of_week].append({
                'aktivitet': activity['aktivitet'],
                'poeng': activity['poeng']
            })
        
        return week_activities  # Returner aktiviteter for hver dag i uken
                
    def fyll_skjermen(self, week_activities):

        if week_activities[0]:
            self.man_button.text = str(week_activities[0][0]['poeng'])
            self.man_button.foreground = self.get_farge(self.man_button.text)
            self.man_akt_label.text = week_activities[0][0]['aktivitet']
        else:
            self.man_button.text = "0"
            self.man_button.foreground = self.get_farge("0")
            self.man_akt_label.text = ""
    
        if week_activities[1]:
            self.tir_button.text = str(week_activities[1][0]['poeng'])
            self.tir_akt_label.text = week_activities[1][0]['aktivitet']
        else:
            self.tir_button.text = "0"
            self.tir_akt_label.text = ""
    
        if week_activities[2]:
            self.ons_button.text = str(week_activities[2][0]['poeng'])
            self.ons_akt_label.text = week_activities[2][0]['aktivitet']
        else:
            self.ons_button.text = "0"
            self.ons_akt_label.text = ""
    
        if week_activities[3]:
            self.tor_button.text = str(week_activities[3][0]['poeng'])
            self.tor_akt_label.text = week_activities[3][0]['aktivitet']
        else:
            self.tor_button.text = "0"
            self.tor_akt_label.text = ""
    
        if week_activities[4]:
            self.fre_button.text = str(week_activities[4][0]['poeng'])
            self.fre_akt_label.text = week_activities[4][0]['aktivitet']
        else:
            self.fre_button.text = "0"
            self.fre_akt_label.text = ""
    
        if week_activities[5]:
            self.lor_button.text = str(week_activities[5][0]['poeng'])
            self.lor_akt_label.text = week_activities[5][0]['aktivitet']
        else:
            self.lor_button.text = "0"
            self.lor_akt_label.text = ""
    
        if week_activities[6]:
            print('søndag:',week_activities[6])
            self.son_button.text = str(week_activities[6][0]['poeng'])
            self.son_akt_label.text = week_activities[6][0]['aktivitet']
        else:
            self.son_button.text = "0"
            self.son_akt_label.text = ""

          
    def lagre_aktivitet(self, dato, aktivitet, poeng):
        try:
            result = anvil.server.call('lagre_aktivitet', dato, aktivitet, poeng)
            print(result)
        except Exception as e:
            print(f"Error saving activity: {e}")
          
    def get_farge(self, poeng_verdi):
      # Definerer farge for hver verdi
      farge_mapping = {
          "0": "BLACK",
          "1": "RED",
          "2": "ORANGE",
          "3": "GREEN"
      }
      return farge_mapping.get(poeng_verdi, "BLACK")

    def regler_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Regler")

    def veil_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Brukerveiledning")

    def individuell_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Resultat_individuell")

    def team_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Resultat_team")

    def trekning_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Trekninger")
