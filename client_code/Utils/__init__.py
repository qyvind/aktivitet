from ._anvil_designer import UtilsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.tables import app_tables
from datetime import timedelta

from .. import Globals


class Utils:

    @staticmethod
    def hent_konkurranse():
        records = app_tables.konkurranse.search(record=1)
        return records[0] if records else None
      
    @staticmethod
    def hent_brukernavn():
        print('hent_brukernavn')
        user = Globals.bruker
        if not user:
            raise Exception("Bruker ikke logget inn")
        
        record = app_tables.userinfo.get(user=user)
        
        if record is None:
            return {"navn": "", "team": "", "lock": False, "leage": "", "ikon": ""}
    
        record_dict = dict(record)
        navn = record_dict.get('navn', "")
    
        team_navn = ""
        lock_status = False
    
        if record_dict.get('team'):
            team_row = record['team']
            team_navn = team_row['team']
            lock_status = team_row['lock']
    
        leage_navn = ""
        ikon_url = ""
        if record_dict.get('leage'):
            leage_row = record['leage']
            leage_navn = leage_row['leage']  # eller 'navn' hvis det er navnet på ligaen
            ikon_url = leage_row['ikon']     # for eksempel en URL eller media-objekt
    
        return {
            "navn": navn,
            "team": team_navn,
            "lock": lock_status,
            "leage": leage_navn,
            "leage_ikon": ikon_url
        }

    @staticmethod
    def hent_poengsummer():
        poeng_dict = {}
    
        for userinfo_rad in app_tables.userinfo.search():
            deltager = userinfo_rad['user']
            if deltager:
                poeng_dict[deltager] = 0
    
        for rad in app_tables.aktivitet.search():
            deltager = rad['deltager']
            poeng = rad['poeng']
            if deltager:
                poeng_dict[deltager] = poeng_dict.get(deltager, 0) + poeng
    
        resultat = []
        for deltager, poeng in poeng_dict.items():
            userinfo_rad = app_tables.userinfo.get(user=deltager)
            navn = userinfo_rad['navn'] if userinfo_rad else None
            email = deltager['email']
            admin = userinfo_rad['admin'] if userinfo_rad else False
            longest_streak = userinfo_rad['longest_streak'] if userinfo_rad and userinfo_rad['longest_streak'] is not None else 0
            bonus = userinfo_rad['bonus'] if userinfo_rad and userinfo_rad['bonus'] is not None else 0
            score = ((poeng + bonus) * 100) + longest_streak
    
            team = userinfo_rad['team']['team'] if userinfo_rad and userinfo_rad['team'] else "Ingen team"
    
            # Hent fra leage riktig
            leage_navn = ""
            ikon = ""
            if userinfo_rad and userinfo_rad['leage']:
                leage_row = userinfo_rad['leage']
                leage_navn = leage_row['leage']  # <-- FELTNAVN må stemme!
                ikon = leage_row['ikon']
    
            resultat.append({
                "deltager": navn if navn else email,
                "navn": navn,
                "email": email,
                "poeng": poeng,
                "longest_streak": longest_streak,
                "bonus": bonus,
                "score": score,
                "team": team,
                "admin": admin,
                "leage": leage_navn,
                "leage_ikon": ikon,
                "user_record": deltager
            })
    
        resultat.sort(key=lambda x: x["score"], reverse=True)
        #print(resultat)
        return resultat

      

    @staticmethod
    def hent_poengsummer_uten_null():
        resultat = [r for r in Utils.hent_poengsummer() if r['poeng'] > 0]
        return resultat

    @staticmethod
    def hent_team_poengsummer():
        team_poeng = {}
        team_lock_map = {}

        for team in app_tables.team.search():
            team_navn = team['team']
            team_poeng[team_navn] = 0
            team_lock_map[team_navn] = team['lock']

        for userinfo in app_tables.userinfo.search():
            team = userinfo['team']
            bruker = userinfo['user']
            #score = userinfo['score']
            longest_streak = userinfo['longest_streak']
            bonus = userinfo['bonus']
            if team and bruker:
                team_navn = team['team']
                bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
                team_poeng[team_navn] += bruker_poeng

        resultat = [
            {
                "team": team,
                "poengsum": poeng,
                "longest_streak": longest_streak,
                "bonus": bonus,
                "lock": team_lock_map.get(team, False)
            }
            for team, poeng in team_poeng.items()
        ]

        resultat.sort(key=lambda x: x["poengsum"], reverse=True)
        return resultat

    @staticmethod
    def hent_teammedlemmer(team_navn):
        team_record = app_tables.team.get(team=team_navn)
        if not team_record:
            return []

        medlemmer = app_tables.userinfo.search(team=team_record)
        team_liste = []
        for member in medlemmer:
            bruker = member['user']
            if not bruker:
                continue
            navn = member['navn']
            poengsum = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
            team_liste.append({"navn": navn, "poeng": poengsum, "user": bruker})

        return team_liste

    # @staticmethod
    # def hent_prompter():
    #     return list(app_tables.ai_prompt.search())

    @staticmethod
    def hent_skritt_first():
        from anvil.tables import app_tables
        user = Globals.bruker
    
        if not user:
            return False
   
        userinfo_rad = app_tables.userinfo.get(user=user)
        if not userinfo_rad:
            return False

        return bool(userinfo_rad['skritt_first'])
    
    @staticmethod
    def vis_tildelte_badges(bruker):
    
        user_badger = app_tables.user_badges.search(user=bruker)
        for rad in user_badger:
            badge = rad['badge']
            badge_id = badge['id']
            #print(f" - Har badge {badge_id}: {badge['name']}")
    
            badge_komponent = getattr(self, f"badge_{badge_id}", None)
            if badge_komponent:
                self.badge_flow_panel.visible = True
                badge_komponent.visible = True

    @staticmethod
    def hent_ny_aktivitet():
        rader = app_tables.ny_aktivitet.search()
        resultat = []
    
        offset = timedelta(hours=2)
    
        for rad in rader:
            tidspunkt_norsk = rad['dato'] + offset
            tidspunkt_str = tidspunkt_norsk.strftime("%d.%m.%Y %H:%M")
    
            resultat.append({
                'email': rad['user']['email'] if rad['user'] else 'Ukjent',
                'dato': tidspunkt_str,
                'aktivitet': rad['aktivitet'],
                'behandlet': rad['behandlet'],
                'row': rad  # 👈 Denne gjør magien!
            })
    
        return resultat


    @staticmethod
    def is_admin():
        print('is_admin')
        user = Globals.bruker
        if user is None:
            return False
        
        # Slå opp brukerens info i userinfo-tabellen
        userinfo = app_tables.userinfo.get(user=user)
        if userinfo and userinfo['admin'] :
            Globals.admin=True
            return True
        return False