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
            
            
            deltagernavn = user['navn']
            # Brukeren er logget inn
            
            if not deltagernavn :
                # Feltet 'navn' er tomt
                self.spor_om_navn()
                user = anvil.users.get_user()
            self.deltager_label.text = user['navn']
            self.login_card.visible = False
            self.loggbok_card.visible = True
            #self.konkurransenavn.text,self.fradato.text, self.tildato.text = self.hent_konkurranse_info()

            konkurransenavn, fradato, tildato = self.hent_konkurranse_info()
            
            if fradato:
                fradato = fradato.strftime("%d.%m.%Y")
            if tildato:
                tildato = tildato.strftime("%d.%m.%Y")
            self.konkurransenavn.text = konkurransenavn
            self.fradato.text = fradato
            self.tildato.text = tildato

        else:
            self.loggbok_card.visible = False
            self.login_card.visible = True



    def initier_uke(self,week_offset):
        self.get_week_info(week_offset)
        self.uke_label.text = self.get_week_range(week_offset)
        week_activities = self.get_activities_for_week()
        self.fyll_skjermen(week_activities)
        
      
    def update_button_state(self, button, label, dato,columnpanel):
        """Oppdaterer knappens tekst og farge basert på nåværende tilstand"""
        states = {
            "0": ("1", "BLACK","LIGHTGREEN"),
            "1": ("2", "BLACK","GREEN"),
            "2": ("3", "BLACK","DARKGREEN"),
            "3": ("0", "BLACK","WHITE"),
        }
      
        previous_state = button.text

        if button.text in states:
            button.text, button.foreground, columnpanel.background = states[button.text]
        else:
            print("button not in states")
              # Initialiser text_box med en default-verdi
        text_box = type('Dummy', (object,), {"text": ""})()  # Oppretter et objekt med et tomt text-attributt
        if button.text == "1":
            """Viser en popup for å spørre om tekst og oppdaterer en label"""
            text_box = TextBox(placeholder="Skriv her...",text=label.text)
    
            result = anvil.alert(
                content=text_box,
                title="Skriv inn type aktivitet",
                buttons=["OK", "Avbryt"]
            )
    
            if result == "OK":  # Hvis brukeren trykket "OK"
                label.text = text_box.text  # Hent tekst fra TextBox og sett den i riktig label
                # Lagre aktiviteten med riktig dato
        
        self.lagre_aktivitet(dato, text_box.text, int(button.text))
            # Hvis knappens tilstand gikk fra 0 til 1, kall sjekken
        if previous_state == "0" and button.text == "1":
            if self.sjekk_lykkehjul():
              self.lykkehjul.visible = True
              week_info = self.get_week_info(self.week_offset_label.text)
              mandag_dato = week_info['monday_date']
              anvil.server.call('lagre_trekning', mandag_dato)
        elif previous_state=="3" and button.text=="0":
            if not self.sjekk_lykkehjul():
              self.lykkehjul.visible = False
              week_info = self.get_week_info(self.week_offset_label.text)
              mandag_dato = week_info['monday_date']
              anvil.server.call('slett_trekning', mandag_dato)
            


    def man_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        mandag_dato = week_info['monday_date']
        self.update_button_state(self.man_button, self.man_akt_label, mandag_dato,self.man_column_panel)

    def tir_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        tirsdag_dato = week_info['monday_date'] + timedelta(days=1)
        self.update_button_state(self.tir_button, self.tir_akt_label, tirsdag_dato,self.tir_column_panel)

    def ons_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        onsdag_dato = week_info['monday_date'] + timedelta(days=2)
        self.update_button_state(self.ons_button, self.ons_akt_label, onsdag_dato,self.ons_column_panel)
    
    def tor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        torsdag_dato = week_info['monday_date'] + timedelta(days=3)
        self.update_button_state(self.tor_button, self.tor_akt_label, torsdag_dato,self.tor_column_panel)
    
    def fre_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        fredag_dato = week_info['monday_date'] + timedelta(days=4)
        self.update_button_state(self.fre_button, self.fre_akt_label, fredag_dato,self.fre_column_panel)
    
    def lor_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        lordag_dato = week_info['monday_date'] + timedelta(days=5)
        self.update_button_state(self.lor_button, self.lor_akt_label, lordag_dato,self.lor_column_panel)
      
    def son_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        week_info = self.get_week_info(self.week_offset_label.text)
        sondag_dato = week_info['monday_date'] + timedelta(days=6)
        self.update_button_state(self.son_button, self.son_akt_label, sondag_dato,self.son_column_panel)

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
        
        # Definer månednavn
        month_names = {
            1: "jan", 2: "feb", 3: "mars", 4: "april", 5: "mai", 6: "juni",
            7: "juli", 8: "aug", 9: "sep", 10: "okt", 11: "nov", 12: "des"
        }
        
        # Sjekk om mandag og søndag er i samme måned
        if monday_date.month == sunday_date.month:
            result = f"{monday_date.day} - {sunday_date.day} {month_names[monday_date.month]}"
        else:
            result = f"{monday_date.day} {month_names[monday_date.month]} - {sunday_date.day} {month_names[sunday_date.month]}"
        
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
      # Hent ukens info og konkurranseinfo
      week_info = self.get_week_info(self.week_offset_label.text)
      mandag_dato = week_info['monday_date']
      _, konkurranse_fradato, konkurranse_tildato = self.hent_konkurranse_info()
      today_date = datetime.today().date()
      
      # Først sjekker vi om uken ligger utenfor konkurranseintervallet
      if not self.er_dato_i_interval(mandag_dato, konkurranse_fradato, konkurranse_tildato):
          # Utenfor intervallet: sett alle kolonnepaneler til rød og deaktiver knappene
          self.man_column_panel.background = "RED"
          self.tir_column_panel.background = "RED"
          self.ons_column_panel.background = "RED"
          self.tor_column_panel.background = "RED"
          self.fre_column_panel.background = "RED"
          self.lor_column_panel.background = "RED"
          self.son_column_panel.background = "RED"
          self.man_button.enabled = False
          self.tir_button.enabled = False
          self.ons_button.enabled = False
          self.tor_button.enabled = False
          self.fre_button.enabled = False
          self.lor_button.enabled = False
          self.son_button.enabled = False
      else:
          # Uken er innenfor konkurranseintervallet, oppdater hver dag og sjekk for fremtid
          # Mandag (offset 0)
          if week_activities[0]:
              self.man_button.text = str(week_activities[0][0]['poeng'])
              self.man_column_panel.background = self.get_farge(self.man_button.text)
              self.man_akt_label.text = week_activities[0][0]['aktivitet']
          else:
              self.man_button.text = "0"
              self.man_column_panel.background = self.get_farge("0")
              self.man_akt_label.text = ""
          # Sjekk om mandag er en fremtidig dato
          self.man_button.enabled = not (mandag_dato > today_date)
      
          # Tirsdag (offset 1)
          tirsdag_dato = mandag_dato + timedelta(days=1)
          if week_activities[1]:
              self.tir_button.text = str(week_activities[1][0]['poeng'])
              self.tir_column_panel.background = self.get_farge(self.tir_button.text)
              self.tir_akt_label.text = week_activities[1][0]['aktivitet']
          else:
              self.tir_button.text = "0"
              self.tir_column_panel.background = self.get_farge("0")
              self.tir_akt_label.text = ""
          self.tir_button.enabled = not (tirsdag_dato > today_date)
      
          # Onsdag (offset 2)
          onsdag_dato = mandag_dato + timedelta(days=2)
          if week_activities[2]:
              self.ons_button.text = str(week_activities[2][0]['poeng'])
              self.ons_column_panel.background = self.get_farge(self.ons_button.text)
              self.ons_akt_label.text = week_activities[2][0]['aktivitet']
          else:
              self.ons_button.text = "0"
              self.ons_column_panel.background = self.get_farge("0")
              self.ons_akt_label.text = ""
          self.ons_button.enabled = not (onsdag_dato > today_date)
      
          # Torsdag (offset 3)
          torsdag_dato = mandag_dato + timedelta(days=3)
          if week_activities[3]:
              self.tor_button.text = str(week_activities[3][0]['poeng'])
              self.tor_column_panel.background = self.get_farge(self.tor_button.text)
              self.tor_akt_label.text = week_activities[3][0]['aktivitet']
          else:
              self.tor_button.text = "0"
              self.tor_column_panel.background = self.get_farge("0")
              self.tor_akt_label.text = ""
          self.tor_button.enabled = not (torsdag_dato > today_date)
      
          # Fredag (offset 4)
          fredag_dato = mandag_dato + timedelta(days=4)
          if week_activities[4]:
              self.fre_button.text = str(week_activities[4][0]['poeng'])
              self.fre_column_panel.background = self.get_farge(self.fre_button.text)
              self.fre_akt_label.text = week_activities[4][0]['aktivitet']
          else:
              self.fre_button.text = "0"
              self.fre_column_panel.background = self.get_farge("0")
              self.fre_akt_label.text = ""
          self.fre_button.enabled = not (fredag_dato > today_date)
      
          # Lørdag (offset 5)
          lordag_dato = mandag_dato + timedelta(days=5)
          if week_activities[5]:
              self.lor_button.text = str(week_activities[5][0]['poeng'])
              self.lor_column_panel.background = self.get_farge(self.lor_button.text)
              self.lor_akt_label.text = week_activities[5][0]['aktivitet']
          else:
              self.lor_button.text = "0"
              self.lor_column_panel.background = self.get_farge("0")
              self.lor_akt_label.text = ""
          self.lor_button.enabled = not (lordag_dato > today_date)
      
          # Søndag (offset 6)
          sondag_dato = mandag_dato + timedelta(days=6)
          if week_activities[6]:
              self.son_button.text = str(week_activities[6][0]['poeng'])
              self.son_column_panel.background = self.get_farge(self.son_button.text)
              self.son_akt_label.text = week_activities[6][0]['aktivitet']
          else:
              self.son_button.text = "0"
              self.son_column_panel.background = self.get_farge("0")
              self.son_akt_label.text = ""
          self.son_button.enabled = not (sondag_dato > today_date)
      self.lykkehjul.visible =   self.sjekk_lykkehjul()      
      

          
    def lagre_aktivitet(self, dato, aktivitet, poeng):
        try:
            result = anvil.server.call('lagre_aktivitet', dato, aktivitet, poeng)
            print(result)
        except Exception as e:
            print(f"Error saving activity: {e}")
          
    def get_farge(self, poeng_verdi):
      # Definerer farge for hver verdi
      farge_mapping = {
          "0": "WHITE",
          "1": "LIGHTGREEN",
          "2": "GREEN",
          "3": "DARKGREEN"
      }
      return farge_mapping.get(poeng_verdi, "WHITE")

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
      
    def hent_konkurranse_info(self):
        # Kall serverfunksjonen for å hente den første posten
        record = anvil.server.call('hent_konkurranse')
        # Dersom record finnes, trekk ut feltene og returner dem
        if record:
            konkurransenavn = record['konkurransenavn']
            fradato = record['fradato']
            tildato = record['tildato']
            return konkurransenavn, fradato, tildato
        else:
            return None, None, None
    def er_dato_i_interval(self, dato, fradato, tildato):
        """
        Returnerer True dersom 'dato' er innenfor intervallet [fradato, tildato] (inkludert endepunktene),
        ellers False.
        """
        return fradato <= dato <= tildato
      
    def sjekk_lykkehjul(self):
      """
      Sjekker om den påloggede brukeren har aktiviteter med minst ett poeng på fem
      forskjellige dager i inneværende uke.
      
      Returnerer True hvis brukeren har aktiviteter med poeng ≥ 1 på fem eller flere dager,
      ellers False.
      """
      # Hent aktivitetene for uken, en dictionary med nøkler 0 (mandag) til 6 (søndag)
      week_activities = self.get_activities_for_week()
      
      count_days = 0  # Teller antall dager med minst ett poeng
      for day in range(7):
          # Sjekk om det finnes minst én aktivitet for dagen med poeng ≥ 1.
          # Her antas det at feltet 'poeng' er et tall, eventuelt konvertert til int.
          if any(int(activity['poeng']) >= 1 for activity in week_activities.get(day, [])):
              count_days += 1
      return count_days >= 5

    def spor_om_navn(self):
        # Opprett en TextBox for å hente inn navnet
        navn_box = TextBox(placeholder="Skriv inn ditt navn")
        
        # Vis en alert med TextBox-en
        resultat = anvil.alert(
            content=navn_box,
            title="Oppgi ekte navn for å delta i konkurransen",
            buttons=["OK", "Avbryt"]
        )
        
        # Hvis brukeren trykker OK og skriver inn et navn
        if resultat == "OK":
            navn = navn_box.text.strip()
            if navn:
                # Oppdater labelen for deltager
                
                # Eventuelt kan du kalle en serverfunksjon for å lagre navnet:
                anvil.server.call("oppdater_brukernavn", navn)
                
            else:
                anvil.alert("Du må skrive inn navn.")
