week, end_of_week + timedelta(days=1))  # Filtrer på datoer
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
