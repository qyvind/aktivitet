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

        # print(f"Ukenummer: {week_active['week_number']}")
        # print(f"Mandag: {week_active['monday']}")
        # print(f"Søndag: {week_active['sunday']}")


    def initier_uke(self,week_offset):
        week_active = self.get_week_info(week_offset)
        self.uke_label.text = self.get_week_range(week_offset)
        print(f"Ukenummer: {week_active['week_number']}")
        print(f"Mandag: {week_active['monday']}")
        print(f"Søndag: {week_active['sunday']}")
        print(self.get_activities_for_week())
      
    def update_button_state(self, button, label):
        """Oppdaterer knappens tekst og farge basert på nåværende tilstand"""
        states = {
            "0": ("1", "RED"),
            "1": ("2", "ORANGE"),
            "2": ("3", "GREEN"),
            "3": ("0", "BLACK"),
        }

        if button.text == "0":
            """Viser en popup for å spørre om tekst og oppdaterer en label"""
            text_box = TextBox(placeholder="Skriv her...")

            result = anvil.alert(
                content=text_box,
                title="Skriv inn type aktivitet",
                buttons=["OK", "Avbryt"]
            )

            if result == "OK":  # Hvis brukeren trykket "OK"
                label.text = text_box.text  # Hent tekst fra TextBox og sett den i riktig label

        if button.text in states:
            button.text, button.foreground = states[button.text]
        else:
            print("button not in states")

    def son_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.son_button, self.son_akt_label)

    def man_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.man_button, self.man_akt_label)

    def tir_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.tir_button, self.tir_akt_label)

    def ons_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.ons_button, self.ons_akt_label)

    def tor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.tor_button, self.tor_akt_label)

    def fre_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.fre_button, self.fre_akt_label)

    def lor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_button_state(self.lor_button, self.lor_akt_label)

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
            "monday": monday.strftime("%Y-%m-%d"),  # Mandagen
            "sunday": sunday.strftime("%Y-%m-%d")  # Søndagen
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
            return {}  # Returner en tom dictionary hvis ingen er pålogget
    
        # Få datoene for den aktive uken (mandag til søndag)
        week_info = self.get_week_info(self.week_offset_label.text)
        start_of_week = week_info['monday']  # Mandag
        end_of_week = week_info['sunday']  # Søndag
    
        # Hent aktivitetene kun for påloggede bruker innenfor ukens datoer
        activities = app_tables.aktivitet.search(
            q.deltager == user,  # Filtrer på innlogget bruker
            q.dato >= start_of_week,
            q.dato <= end_of_week
        )
    
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
