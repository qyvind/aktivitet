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
from ..PoengVelger import PoengVelger
from ..Utils import Utils
from .. import Globals
from anvil_extras.animation import Effect, Transition
import time




class Loggbok(LoggbokTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        self.vis_nye_badges(Globals.bruker)
        Globals.week_offset = 0
        #self.hent_week_offset() 
        self.initier_uke(Globals.week_offset)
        self.sjekk_bruker()
        


  

    def initier_uke(self,week_offset):
        self.get_week_info(week_offset)
        self.uke_label.text = self.get_week_range(week_offset)
        week_activities = self.get_activities_for_week()
        self.fyll_skjermen(week_activities)
        

    def man_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(0, self.man_button, self.man_akt_label, self.man_ikon, self.man_label, self.man_column_panel.tooltip, self.man_skritt)

    
    def tir_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(1, self.tir_button, self.tir_akt_label, self.tir_ikon,self.tir_label,self.tir_column_panel.tooltip,self.tir_skritt)
    
    def ons_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(2, self.ons_button, self.ons_akt_label,self.ons_ikon, self.ons_label,self.ons_column_panel.tooltip,self.ons_skritt)
    
    def tor_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(3, self.tor_button, self.tor_akt_label, self.tor_ikon,self.tor_label,self.tor_column_panel.tooltip,self.tor_skritt)
    
    def fre_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(4, self.fre_button, self.fre_akt_label,self.fre_ikon, self.fre_label,self.fre_column_panel.tooltip,self.fre_skritt)
    
    def lor_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(5, self.lor_button, self.lor_akt_label, self.lor_ikon,self.lor_label,self.lor_column_panel.tooltip,self.lor_skritt)
    
    def son_button_click(self, **event_args):
        self.åpne_poengvelger_for_dag(6, self.son_button, self.son_akt_label,self.son_ikon, self.son_label,self.son_column_panel.tooltip,self.son_skritt)
    
    
    def åpne_poengvelger_for_dag(self, dag_index, knapp, label,ikon_komponent, ukedag_label, beskrivelse, skritt):
        valgt_poeng = int(knapp.text or 0)
        aktivitet = label.text
        
        def mottak_fra_poengvelger(poeng, aktivitet, nytt_ikon,beskrivelse, ikon_path,skritt=None):
          week_info = self.get_week_info(Globals.week_offset)
          valgt_dato = week_info['monday_date'] + timedelta(days=dag_index)
      
          # Oppdater GUI
          
          if aktivitet == "Hviledag":
            poeng = 0
          knapp.text = str(poeng)
          label.text = aktivitet
          ikon_komponent.source = nytt_ikon
          ikon_komponent.width = 32
          ikon_komponent.height = 32
          ikon_komponent.tooltip = beskrivelse
          if ikon_komponent == None:
            label.visible=True
            ikon_komponent.visible=False
          else:
            label.visible = False
            ikon_komponent.visible = True
      
          # 🧠 Konverter LazyMedia til vanlig Media
          if isinstance(nytt_ikon, anvil.BlobMedia) or nytt_ikon is None:
              ikon_til_server = nytt_ikon
          else:
              ikon_til_server = anvil.BlobMedia(nytt_ikon.content_type, nytt_ikon.get_bytes(), name=nytt_ikon.name)
            
          self.lagre_aktivitet(valgt_dato, aktivitet, poeng, ikon_til_server,beskrivelse,skritt)
      
            

        
        open_form("PoengVelger", valgt_poeng=valgt_poeng, aktivitet=aktivitet, ukedag=ukedag_label.text, ikon=ikon_komponent.source, beskrivelse=beskrivelse, callback=mottak_fra_poengvelger)




    def logout_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.users.logout()
        #self.login_card.visible = True
        open_form('Login')


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



    def get_activities_for_week(self):
        # Få den påloggede brukeren
        user = Globals.bruker
        if not user:
            return {day: [] for day in range(7)}  # Returner en dictionary med alle dager
        
        # Få datoene for den aktive uken (mandag til søndag)
        week_info = self.get_week_info(Globals.week_offset)
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
            #print(f"Error fetching activities: {e}")
            return {}
        
        # Organisere aktivitetene i en liste med 7 dager (0=Mandag, 6=Søndag)
        week_activities = {day: [] for day in range(7)}
        
        for activity in activities:
            activity_date = activity['dato']
            day_of_week = activity_date.weekday()  # Mandag = 0, Søndag = 6
            week_activities[day_of_week].append({
                'aktivitet': activity['aktivitet'],
                'poeng': activity['poeng'],
                'ikon': activity['ikon'],
                'beskrivelse': activity['beskrivelse'],
                'skritt': activity['skritt'] ,
            })
        
        return week_activities  # Returner aktiviteter for hver dag i uken
                
    def fyll_skjermen(self, week_activities):
      # Hent ukens info og konkurranseinfo
      week_info = self.get_week_info(Globals.week_offset)
      mandag_dato = week_info['monday_date']
      _, konkurranse_fradato, konkurranse_tildato = self.hent_konkurranse_info()

      # Sjekk om vi er på første uke i konkurransen
      if mandag_dato == konkurranse_fradato:
          self.prev_week_button.visible = False  # Skjul pil til forrige uke
      else:
          self.prev_week_button.visible = True  # Vis pil ellers

      # Sjekk om vi er på siste uke i konkurransen
      sondag_dato = mandag_dato + timedelta(days=6)
      if sondag_dato == konkurranse_tildato:
          self.next_week_button.visible = False  # Skjul pil til neste uke
      else:
          self.next_week_button.visible = True   # Vis pil ellers

      
      # 👇 Bruker JavaScript Date-objekt for å få lokal "i dag"-dato fra klientens tidssone
      import anvil.js
      js_now = anvil.js.window.Date() 
      today_date = datetime.fromtimestamp(js_now.getTime() / 1000).date()
  
      # Først sjekker vi om uken ligger utenfor konkurranseintervallet
      if not self.er_dato_i_interval(mandag_dato, konkurranse_fradato, konkurranse_tildato):
          # Utenfor intervallet: sett alle kolonnepaneler til rød og deaktiver knappene
          for panel, knapp in [
              (self.man_column_panel, self.man_button),
              (self.tir_column_panel, self.tir_button),
              (self.ons_column_panel, self.ons_button),
              (self.tor_column_panel, self.tor_button),
              (self.fre_column_panel, self.fre_button),
              (self.lor_column_panel, self.lor_button),
              (self.son_column_panel, self.son_button),
          ]:
              panel.background = "RED"
              knapp.enabled = False
      else:
          # Uken er innenfor konkurranseintervallet, oppdater hver dag og sjekk for fremtid
          base_dato = mandag_dato
          komponenter = [
              (self.man_button, self.man_column_panel, self.man_akt_label, week_activities[0], base_dato, self.man_ikon,self.man_skritt,self.man_column_panel),
              (self.tir_button, self.tir_column_panel, self.tir_akt_label, week_activities[1], base_dato + timedelta(days=1), self.tir_ikon,self.tir_skritt,self.tir_column_panel),
              (self.ons_button, self.ons_column_panel, self.ons_akt_label, week_activities[2], base_dato + timedelta(days=2), self.ons_ikon,self.ons_skritt,self.ons_column_panel),
              (self.tor_button, self.tor_column_panel, self.tor_akt_label, week_activities[3], base_dato + timedelta(days=3), self.tor_ikon,self.tor_skritt,self.tor_column_panel),
              (self.fre_button, self.fre_column_panel, self.fre_akt_label, week_activities[4], base_dato + timedelta(days=4), self.fre_ikon,self.fre_skritt,self.fre_column_panel),
              (self.lor_button, self.lor_column_panel, self.lor_akt_label, week_activities[5], base_dato + timedelta(days=5), self.lor_ikon,self.lor_skritt,self.lor_column_panel),
              (self.son_button, self.son_column_panel, self.son_akt_label, week_activities[6], base_dato + timedelta(days=6), self.son_ikon,self.son_skritt,self.son_column_panel),
          ]
          
          
          for knapp, panel, label, akt_data, dato, ikon_komponent,skritt_komponent, ColumnPanel in komponenter:
              self.oppdater_dag(knapp, panel, label, akt_data, dato, today_date, ikon_komponent,skritt_komponent, ColumnPanel)

  
      progress = self.sjekk_lykkehjul()
      if progress >=100:
        self.lykke_bw_image.visible = False
        self.lykke_color_image.visible = True 
        self.lykke_indikator.progress_color = "green"
      else:
        self.lykke_bw_image.visible = True
        self.lykke_color_image.visible = False
        self.lykke_indikator.progress_color = "red"
      self.lykke_indikator.progress = progress
      
      #user = anvil.users.get_user()
      self.vis_tildelte_badges(Globals.bruker)

  


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



          
    def lagre_aktivitet(self, dato, aktivitet, poeng, ikon, beskrivelse,skritt=None):
        try:
            print('vil lagre skritt',skritt)
            result = anvil.server.call('lagre_aktivitet', dato, aktivitet, poeng, ikon, beskrivelse,skritt)
            print(result)
            # AI oppmuntring:          
            # # ✅ Sjekk om datoen er i dag
            # from datetime import date
            # if dato == date.today():
            #     melding = anvil.server.call('generer_oppmuntring_for_bruker')
            #     if melding:
            #         alert(melding, title="💬 Framskritt:")
        except Exception as e:
            print(f"Error saving activity: {e}")

            
          
    def get_farge(self, poeng_verdi):
        farge_mapping = {
            "0": "#e0e0e0",     # Nøytral grå
            "1": "#b2f2bb",     # Lys grønn
            "2": "#69db7c",     # Middels grønn
            "3": "#2b8a3e"      # Mørk grønn
        }
        return farge_mapping.get(poeng_verdi, "#e0e0e0")



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
      week_info = self.get_week_info(Globals.week_offset)
      #print(week_info)
      open_form("Trekninger", week_info['monday_date'])
      
    def hent_konkurranse_info(self):
        # Kall serverfunksjonen for å hente den første posten
        record = Utils.hent_konkurranse()
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
      return count_days *20

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
        return(navn)


    def sjekk_bruker(self):
        user = Globals.bruker
        # if Globals.admin:
        #   self.admin_button.visible = True
        # else:
        #   self.admin_button.visible = False
        
        if user:
            # Hent oppdaterte brukerdata fra UserInfo-tabellen
            deltagerdata= Utils.hent_brukernavn()
            
            #print(deltagerdata)
            navn=deltagerdata['navn']
            team=deltagerdata['team']
            if deltagerdata['leage']:
              leage_ikon = deltagerdata['leage_ikon']
              leage = deltagerdata['leage']
              
            else:
              leage_ikon = " "
              leage = " "
            # print(navn, team)
            self.deltager_label.text = deltagerdata['navn']
            self.team_label.text = deltagerdata['team']
            self.leage_ikon.text = leage_ikon
            self.leage_ikon.tooltip = f"Liga: {leage}"
            

              
            
    
            if not navn or navn.strip() == "":  # Forhindrer at None eller tom streng trigger navnespørsmål
                # Feltet 'navn' er tomt – spør om navn
                navn = self.spor_om_navn()
                self.deltager_label.text = navn
    
            
            #self.login_card.visible = False
            self.loggbok_card.visible = True
    
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
            #self.login_card.visible = True


    def login_click(self, **event_args):
        """Kalles når brukeren trykker logg inn-knappen"""
        user = anvil.users.login_with_form(allow_remembered=30, allow_cancel=True)
        if user:
            self.sjekk_bruker()  # Oppdater UI med riktig navn fra UserInfo

    def team_label_click(self,  **event_args):
      """This method is called when the button is clicked"""
      open_form('team_medlemmer',teamnavn=self.team_label.text)


    def oppdater_dag(self, knapp, panel, label, aktivitet_data, dato, today_date, ikon_komponent,skritt_komponent, column_panel):
        if aktivitet_data:
            poeng = str(aktivitet_data[0]['poeng'])
            aktivitet = aktivitet_data[0]['aktivitet']
            ikon = aktivitet_data[0]['ikon']
            column_panel.tooltip = aktivitet_data[0]['beskrivelse']
            skritt_komponent.text = aktivitet_data[0]['skritt']
        else:
            poeng = "0"
            aktivitet = ""
            ikon = None
            column_panel.tooltip = ""
    
        if ikon_komponent is not None:
            ikon_komponent.source = ikon
    
        knapp.text = poeng
        if poeng == "0" and not aktivitet and dato <= today_date and ikon is None:
            label.text = "Hviledag"
        else:
            label.text = aktivitet

          
    
        mandag_denne_uken = today_date - timedelta(days=today_date.weekday())
        mandag_forrige_uke = mandag_denne_uken - timedelta(weeks=1)
    
        # --- START: Logikk for å bestemme om dagen er redigerbar ---
        mandag_denne_uken = today_date - timedelta(days=today_date.weekday())
        mandag_forrige_uke = mandag_denne_uken - timedelta(weeks=1)

        er_fremtid = dato > today_date
        ''' # Avsnittet under åpnet for redigering av inneværende uke + forrige hvis det er mandag
        er_redigerbar_uke = False
        # Sjekk 1: Er datoen i inneværende uke eller senere?
        if dato >= mandag_denne_uken:
            er_redigerbar_uke = True
        # Sjekk 2: Er datoen i forrige uke OG er det mandag i dag?
        elif dato >= mandag_forrige_uke and today_date.weekday() == 0:
             er_redigerbar_uke = True
        # Ellers (eldre enn forrige uke, eller forrige uke på en annen dag enn mandag)
        # er er_redigerbar_uke fortsatt False
        '''

        if self.sjekk_korrigering():
          #korrigering av tidligere datoer tillatt
          er_redigerbar_uke = True
        else:
          er_redigerbar_uke = dato >= (today_date - timedelta(days=1))

        # Knappen skal være aktivert hvis det IKKE er fremtid OG uken er redigerbar
        knapp.enabled = (not er_fremtid) and er_redigerbar_uke
        # --- SLUTT: Logikk for å bestemme om dagen er redigerbar ---


      
        knapp.enabled = (not er_fremtid) and er_redigerbar_uke
    
        # --- Oppdatert farge- og stilsetting ---
        if not knapp.enabled:
            if dato < today_date:
                panel.background_color = self.get_farge(poeng) if poeng != "0" else "#f5f5f5"
            else:
                panel.background_color = "#eeeeee"
            knapp.foreground = "#aaaaaa"
            label.foreground = "#aaaaaa"
            ikon_komponent.foreground = "#aaaaaa"
            #panel.border = "1px dashed #cccccc"
            panel.opacity = 1.0  # Evt. sett til 0.7 hvis du vil tone det mer ned
        else:
            panel.background_color = "#e0e0e0" if poeng == "0" else self.get_farge(poeng)
            knapp.foreground = "black"
            label.foreground = "black"
            ikon_komponent.foreground = "black"
            #panel.border = "2px dashed #0077cc"
            panel.opacity = 1.0
    
        knapp.style = ""
        label.style = ""


    def deltager_label_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('minside')

    def admin_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin')



    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.image_1.source = app_files.swimming.png


    def button_1_click(self, **event_args):
      self.liga_image.source = "_/theme/rsz_bronse_tr.png"



    def vis_nye_badges(self,bruker):
        nye_badger = app_tables.user_badges.search(user=bruker, informert=False)
    
        for rad in nye_badger:
            badge = rad['badge']
            badgenummer = badge['id']
            beskrivelse = badge['description']
            poeng = badge['bonus'] or 0
            alertmessage = anvil.server.call('generer_badge_melding',badgenummer)
            alert(
                alertmessage,
                title="Ny prestasjon oppnådd!",
                large=True
            )
    
            rad.update(informert=True)

    def sjekk_korrigering(self,**event_args):
        konkurranse = app_tables.konkurranse.search()[0]  # Forutsetter én rad
        return konkurranse['korrigering']

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

    def leage_ikon_click(self, **event_args):
      alert(self.leage_ikon.tooltip)
