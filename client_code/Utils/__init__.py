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
        print('Utils_hent_brukernavn')
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
        resultat = []
    
        for userinfo_rad in app_tables.userinfo.search():
            deltager = userinfo_rad['user']
    
            if not deltager:
                continue
    
            navn = userinfo_rad['navn'] or deltager['email']
            email = deltager['email']
            poeng = userinfo_rad['poeng'] or 0
            bonus = userinfo_rad['bonus'] or 0
            longest_streak = userinfo_rad['longest_streak'] or 0
            score = userinfo_rad['score'] or 0
            admin = userinfo_rad['admin'] or False
    
            team = "Ingen team"
            if userinfo_rad['team']:
                team = userinfo_rad['team']['team']
    
            leage_navn = ""
            ikon = ""
            if userinfo_rad['leage']:
                leage_row = userinfo_rad['leage']
                leage_navn = leage_row['leage']
                ikon = leage_row['ikon']
    
            resultat.append({
                "deltager": navn,
                "navn": navn,
                "email": email,
                "poeng": poeng,
                "bonus": bonus,
                "longest_streak": longest_streak,
                "score": score,
                "team": team,
                "admin": admin,
                "leage": leage_navn,
                "leage_ikon": ikon,
                "user_record": deltager
            })
    
        resultat.sort(key=lambda x: x["score"], reverse=True)
        return resultat

          

    @staticmethod
    def hent_poengsummer_uten_null():
        resultat = [r for r in Utils.hent_poengsummer() if r['poeng'] > 0]
        return resultat

    @staticmethod
    def hent_team_poengsummer():
        resultat = []
    
        for team in app_tables.team.search():
            team_navn = team['team']
            poeng = team['poeng'] or 0
            bonus = team['bonus'] or 0
            longest_streak = team['longest_streak'] or 0
            score = team['score'] or 0
            members = team['members'] or 0
            lock = team['lock'] or False
    
            resultat.append({
                "team": team_navn,
                "poengsum": poeng,
                "longest_streak": longest_streak,
                "bonus": bonus,
                "score": score,
                "members": members,
                "lock": lock
            })
    
        # Sorter på score, høyest først
        resultat.sort(key=lambda x: x["score"], reverse=True)
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