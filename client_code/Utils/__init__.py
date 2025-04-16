from ._anvil_designer import UtilsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.tables import app_tables

class Utils:

    @staticmethod
    def hent_konkurranse():
        records = app_tables.konkurranse.search(record=1)
        return records[0] if records else None

    # @staticmethod
    # def hent_brukernavn(user):
    #     record = app_tables.userinfo.get(user=user)
    #     if record is None:
    #         return {"navn": "", "team": "", "lock": False}

    #     navn = record.get('navn', "")
    #     team_navn = record['team']['team'] if record.get('team') else ""
    #     lock_status = record['team']['lock'] if record.get('team') else False

    #     return {
    #         "navn": navn,
    #         "team": team_navn,
    #         "lock": lock_status
    #     }

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
            longest_streak = userinfo_rad['longest_streak']
            score = userinfo_rad['score']
            print('streak',navn,longest_streak)
            team = userinfo_rad['team']['team'] if userinfo_rad and userinfo_rad['team'] else "Ingen team"

            resultat.append({
                "deltager": navn if navn else email,
                "navn": navn,
                "email": email,
                "poeng": poeng,
                "longest_streak": longest_streak,
                "score": score,
                "team": team,
                "admin": admin
            })

        resultat.sort(key=lambda x: x["poeng"], reverse=True)
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
            score = userinfo['score']
            longest_streak = userinfo['longest_streak']
            if team and bruker:
                team_navn = team['team']
                bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
                team_poeng[team_navn] += bruker_poeng

        resultat = [
            {
                "team": team,
                "poengsum": poeng,
                "longest_streak": longest_streak,
                "score": score,
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
