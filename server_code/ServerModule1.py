import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import date, timedelta
import datetime
import openai
from anvil.secrets import get_secret
import time
from collections import defaultdict



@anvil.server.callable

def add_aktivitet(aktivitet):
  print('add_aktivitet')
  
  if aktivitet.get('dato') and aktivitet.get('aktivitet') and aktivitet.get('poeng') :
    app_tables.aktivitet.add_row(**aktivitet)

@anvil.server.callable
def update_aktivitet(aktivitet, aktivitet_data):
  print('update_aktivitet')
  
  if aktivitet_data['dato'] and aktivitet_data['aktivitet'] and aktivitet_data['poeng']: 
    aktivitet.update(**aktivitet_data)

@anvil.server.callable
def delete_aktivitet(aktivitet):
  print('delete_aktivitet')
  aktivitet.delete()

@anvil.server.callable
def batch_create_users(user_list):
    print('batch_create_users')

    if not isinstance(user_list, list):
        #print("Feil: Forventet en liste over brukere, men fikk noe annet.")
        return "Feil: Dataformat er ikke gyldig."

    for user in user_list:
        try:
            email = user["email"].strip().lower()  # Normaliser e-post for sammenligning
            password = user["password"]
            navn = user.get("navn", "")

            # Feilsøk: Logg søket
            existing_users = list(app_tables.users.search())  # Hent alle brukere
            matching_users = [u for u in existing_users if u['email'].strip().lower() == email]

            if matching_users:
                #print(f"Bruker {email} finnes allerede, hopper over.")
                continue

            # Opprett ny bruker
            anvil.users.signup_with_email(email, password)
            #print(f"Bruker {email} opprettet.")

            # Hent den opprettede brukeren igjen
            created_user = app_tables.users.get(email=email)
            if created_user:
                app_tables.userinfo.add_row(user=created_user, navn=navn)
                #print(f"Bruker {email} opprettet med navn {navn}.")
            else:
                print(f"Kunne ikke finne brukeren {email} etter opprettelse.")

        except KeyError as e:
            print(f"Feil: Manglende nøkkel {e} i brukerdata: {user}")
        except Exception as e:
            print(f"Uventet feil for bruker {user}: {e}")

    return "Alle brukere er lagt til!"




@anvil.server.callable
def lagre_aktivitet(dato, aktivitet, poeng, ikon,beskrivelse,skritt=None):

    print('lagre_aktivitet', skritt)
    user = anvil.users.get_user()
    if not user:
        raise Exception("Ingen bruker er pålogget")
    
    # Sjekk om det allerede finnes en post for den aktuelle datoen og brukeren
    existing_activity = app_tables.aktivitet.get(deltager=user, dato=dato)
    
    if existing_activity:
        # Oppdater den eksisterende posten
        existing_activity.update(aktivitet=aktivitet, poeng=poeng,ikon=ikon, beskrivelse=beskrivelse,skritt=skritt )
        return "Aktivitet oppdatert"
    else:
        # Lagre ny post i tabellen aktivitet
        app_tables.aktivitet.add_row(
            deltager=user,
            dato=dato,
            aktivitet=aktivitet,
            poeng=poeng,
            ikon=ikon,
            beskrivelse = beskrivelse,
            skritt=skritt
        )
        return "Aktivitet lagret"


# @anvil.server.callable
# def hent_konkurranse():
#     #print('hent_konkurranse')
#     # Hent alle poster med record lik 1
#     konkurranse_records = app_tables.konkurranse.search(record=1)
#     # Returner den første posten dersom den finnes, ellers None
#     return konkurranse_records[0] if konkurranse_records else None

# @anvil.server.callable
# def lagre_trekning(uke_mandag):
#     print('lagre_trekning')
#     # Hent den påloggede brukeren
#     user = anvil.users.get_user()
#     if not user:
#         raise Exception("Bruker ikke logget inn")
    
#     # Sjekk om en record med samme uke og bruker allerede finnes
#     eksisterende = list(app_tables.trekning.search(uke_mandag=uke_mandag, deltager=user))
#     if eksisterende:
#         pass
#     else:
#         # Legg til ny record i tabellen 'trekning'
#         app_tables.trekning.add_row(uke_mandag=uke_mandag, deltager=user)
#     return ()

# @anvil.server.callable
# def slett_trekning(uke_mandag):
#     #print('slett_trekning')
#     # Hent den påloggede brukeren
#     user = anvil.users.get_user()
#     if not user:
#         raise Exception("Bruker ikke logget inn")
    
#     # Sjekk om en record med samme uke og bruker allerede finnes
#     eksisterende = list(app_tables.trekning.search(uke_mandag=uke_mandag, deltager=user))
#     # Dersom record finnes, slett den(e)
#     for row in eksisterende:
#         row.delete()
#     return ()

@anvil.server.callable
def oppdater_brukernavn(nytt_navn):
    print('oppdater_brukernavn')
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")

    record = app_tables.userinfo.get(user=user)

    if record:
        record['navn'] = nytt_navn
    else:
        # Hent ligaen med level = 1
        liga_record = app_tables.ligaer.get(level=1)
        if not liga_record:
            raise Exception("Fant ikke liga med level = 1")
        
        # Opprett ny userinfo med referanse til liga
        app_tables.userinfo.add_row(
            user=user,
            navn=nytt_navn,
            longest_streak=0,
            bonus=0,
            liga=liga_record
        )

    return "Navn oppdatert"



# @anvil.server.callable
# def hent_brukernavn():
#     print('hent_brukernavn')
#     user = anvil.users.get_user()
#     if not user:
#         raise Exception("Bruker ikke logget inn")
    
#     record = app_tables.userinfo.get(user=user)
    
#     if record is None:
#         return {"navn": "", "team": "", "lock": False, "liga": "", "ikon": ""}

#     record_dict = dict(record)
#     navn = record_dict.get('navn', "")

#     team_navn = ""
#     lock_status = False

#     if record_dict.get('team'):
#         team_row = record['team']
#         team_navn = team_row['team']
#         lock_status = team_row['lock']

#     liga_navn = ""
#     ikon_url = ""

#     if record_dict.get('liga'):
#         liga_row = record['liga']
#         liga_navn = liga_row['liga']  # eller 'navn' hvis det er navnet på ligaen
#         ikon_url = liga_row['ikon']     # for eksempel en URL eller media-objekt

#     return {
#         "navn": navn,
#         "team": team_navn,
#         "lock": lock_status,
#         "liga": liga_navn,
#         "liga_ikon": ikon_url
#     }


def hent_poengsummer():
    #print('hent_poengsummer')
    poeng_dict = {}

    # Hent alle brukere og initialiser dem med 0 poeng
    for userinfo_rad in app_tables.userinfo.search():
        deltager = userinfo_rad['user']
        if deltager:
            poeng_dict[deltager] = 0  # Start med 0 poeng

    # Hent alle aktiviteter og summer poeng
    for rad in app_tables.aktivitet.search():
        deltager = rad['deltager']  # Link til user-tabellen
        poeng = rad['poeng']

        if deltager:
            if deltager not in poeng_dict:  # Sikre at deltager er registrert i dict
                poeng_dict[deltager] = 0  
            poeng_dict[deltager] += poeng

    # Konverter til liste med navn, e-post og team
    resultat = []
    for deltager, poeng in poeng_dict.items():
        userinfo_rad = app_tables.userinfo.get(user=deltager)  # Hent userinfo basert på user-link
        navn = userinfo_rad['navn'] if userinfo_rad else None
        email = deltager['email']
        admin = userinfo_rad['admin']
        team = userinfo_rad['team']['team'] if userinfo_rad and userinfo_rad['team'] else "Ingen team"

        # Her lagrer vi poengsummen i userinfo-tabellen
        if userinfo_rad:
            userinfo_rad['poeng'] = poeng
            userinfo_rad['score'] = poeng

        resultat.append({
            "deltager": navn if navn else email,
            "navn": navn,
            "email": email,
            "poeng": poeng,
            "team": team,
            "admin": admin
        })

    resultat.sort(key=lambda x: x["poeng"], reverse=True)
    return resultat




@anvil.server.callable
def hent_ukens_premietrekning(mandag):
    print('hent_ukens_premietrekning')
    import datetime

    if isinstance(mandag, datetime.datetime):
        mandag = mandag.date()

    søndag = mandag + datetime.timedelta(days=6)
    deltager_dager = {}

    for rad in app_tables.aktivitet.search():
        deltager = rad['deltager']
        dato = rad['dato']
        poeng = rad['poeng']

        # Sjekk om datoen er innenfor uke, og poeng er 1, 2 eller 3
        if mandag <= dato <= søndag and 1 <= poeng :
            if deltager:
                if deltager not in deltager_dager:
                    deltager_dager[deltager] = set()
                deltager_dager[deltager].add(dato)

    kvalifiserte = [deltager for deltager, dager in deltager_dager.items() if len(dager) >= 5]

    resultat = []
    for deltager in kvalifiserte:
        userinfo_rad = app_tables.userinfo.get(user=deltager)
        navn = userinfo_rad['navn'] if userinfo_rad else None
        resultat.append(navn if navn else deltager['email'])

    return resultat


@anvil.server.callable
def hent_konsekutive_kvalifiserte(konkurranse_start, konkurranse_slutt):
    print('hent_konsekutive_kvalifiserte')

    import datetime

    if isinstance(konkurranse_start, datetime.datetime):
        konkurranse_start_dato = konkurranse_start.date()
    else:
        konkurranse_start_dato = konkurranse_start

    if isinstance(konkurranse_slutt, datetime.datetime):
        konkurranse_slutt_dato = konkurranse_slutt.date()
    else:
        konkurranse_slutt_dato = konkurranse_slutt

    if konkurranse_start_dato.weekday() != 0:
        raise ValueError("konkurranse_start må være en mandag.")
    if konkurranse_start_dato > konkurranse_slutt_dato:
        return []

    today = datetime.date.today()
    start_of_current_week = today - datetime.timedelta(days=today.weekday())
    siste_fullforte_sondag = start_of_current_week - datetime.timedelta(days=1)
    effektiv_slutt_dato = min(konkurranse_slutt_dato, siste_fullforte_sondag)

    if konkurranse_start_dato > effektiv_slutt_dato:
        return []

    konsekutive_kvalifiserte = None
    gjeldende_mandag = konkurranse_start_dato

    while True:
        gjeldende_søndag = gjeldende_mandag + datetime.timedelta(days=6)

        if gjeldende_søndag > effektiv_slutt_dato:
            break

        deltager_dager_uke = {}
        # KORRIGERT LINJE: Bruker q.greater_than_or_equal_to
        relevante_aktiviteter = app_tables.aktivitet.search(
            dato=q.between(gjeldende_mandag, gjeldende_søndag, min_inclusive=True, max_inclusive=True),
            poeng=q.greater_than_or_equal_to(1) # <-- ENDRING HER
        )

        for rad in relevante_aktiviteter:
            deltager = rad['deltager']
            dato = rad['dato']
            if deltager:
                if deltager not in deltager_dager_uke:
                    deltager_dager_uke[deltager] = set()
                deltager_dager_uke[deltager].add(dato)

        ukens_kvalifiserte_set = {
            deltager for deltager, dager in deltager_dager_uke.items() if len(dager) >= 5
        }

        if konsekutive_kvalifiserte is None:
            konsekutive_kvalifiserte = ukens_kvalifiserte_set
        else:
            konsekutive_kvalifiserte.intersection_update(ukens_kvalifiserte_set)

        if not konsekutive_kvalifiserte:
            break

        gjeldende_mandag += datetime.timedelta(days=7)

    if konsekutive_kvalifiserte is None or not konsekutive_kvalifiserte:
        return []

    resultat = []
    for deltager in konsekutive_kvalifiserte:
        userinfo_rad = app_tables.userinfo.get(user=deltager)
        navn = userinfo_rad['navn'] if userinfo_rad and userinfo_rad['navn'] else None
        resultat.append(navn if navn else deltager['email'])

    return resultat


@anvil.server.callable
def hent_team_poengsummer():
    print('hent_team_poengsummer')
    team_poeng = {}
    team_lock_map = {}  # Ny dict for å lagre lock-status for hvert team

    for team in app_tables.team.search():
        team_navn = team['team']
        team_poeng[team_navn] = 0
        team_lock_map[team_navn] = team['lock']  # Lagre lock-status

    for userinfo in app_tables.userinfo.search():
        team = userinfo['team']
        bruker = userinfo['user']

        if team and bruker:
            team_navn = team['team']
            bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
            team_poeng[team_navn] += bruker_poeng

    resultat = [
        {
            "team": team,
            "poengsum": poeng,
            "lock": team_lock_map.get(team, False)
        }
        for team, poeng in team_poeng.items()
    ]
    resultat.sort(key=lambda x: x["poengsum"], reverse=True)

    print(f"🏆 Totale poengsummer per team: {resultat}")
    return resultat



@anvil.server.callable
def create_user(email, name, password, team_name=None):
    print('create_user')
   # print(f"Oppretter bruker: {email}")

    # Sjekk om brukeren allerede finnes
    existing_users = app_tables.users.search(email=email)
    if len(existing_users) > 0:
        #print(f"Bruker {email} finnes allerede.")
        return "Bruker finnes allerede."

    # Opprett ny bruker med Anvils innebygde metode
    user = anvil.users.signup_with_email(email, password)
    
    if user:
        # Finn team hvis team_name er oppgitt
        team = None
        if team_name:
            team_search = app_tables.team.search(team=team_name)  # Finn team i tabellen
            if team_search:
                team = team_search[0]  # Hent første treff

        # Opprett en relatert record i userinfo-tabellen med team
        app_tables.userinfo.add_row(user=user, navn=name, team=team)

        print(f"Bruker {email} opprettet med navn {name} og team {team_name if team else 'Ingen team valgt'}.")
        return "Bruker opprettet!"
    else:
        print(f"Feil ved opprettelse av bruker {email}.")
        return "Feil ved opprettelse av bruker."

# @anvil.server.callable
# def hent_teammedlemmer(team_navn):
#     #print(f"Henter medlemmer og poeng for team: {team_navn}")
    
#     # Finn team-raden basert på navn
#     team_record = app_tables.team.get(team=team_navn)

#     if not team_record:
#         #print(f"❌ Fant ikke team med navn: {team_navn}")
#         return []

#     # Hent alle brukere i userinfo-tabellen som er tilknyttet dette teamet
#     medlemmer = app_tables.userinfo.search(team=team_record)

#     # Lag en liste med navn og total poengsum basert på aktivitetene deres
#     team_liste = []
#     for member in medlemmer:
#         bruker = member['user']  # Hent bruker-raden (fra users-tabellen)
#         if not bruker:
#             continue  # Hopp over hvis user er None

#         navn = member['navn']  # Hent navn fra userinfo-tabellen

#         # Finn og summer poeng fra aktivitet-tabellen hvor brukeren er deltager
#         poengsum = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
#         user = member['user']
#         # Legg til i listen
#         team_liste.append({"navn": navn, "poeng": poengsum, "user":user})

#     #print(f"🏆 Teammedlemmer i {team_navn}: {team_liste}")
#     return team_liste

@anvil.server.callable
def opprett_nytt_team(team_navn):
    print(f'Oppretter nytt team: {team_navn}')
    
    # Sjekk om teamet allerede finnes
    eksisterende_team = app_tables.team.get(team=team_navn)
    if eksisterende_team:
        print(f"Team {team_navn} finnes allerede.")
        return "Teamet finnes allerede!"
    
    # Opprett nytt team
    app_tables.team.add_row(team=team_navn)
    print(f"Team {team_navn} opprettet!")
    return "Team opprettet!"

@anvil.server.callable
def slett_team(team_navn):
    print(f'Forsøker å slette team: {team_navn}')
    
    # Finn teamet i databasen
    team = app_tables.team.get(team=team_navn)
    if not team:
        #print(f"Team {team_navn} finnes ikke.")
        return "Teamet finnes ikke!"
    
    # Sjekk om det finnes brukere i dette teamet
    medlemmer = app_tables.userinfo.search(team=team)
    if len(medlemmer) > 0:
        #print(f"Kan ikke slette {team_navn}, det har medlemmer.")
        return "Kan ikke slette teamet, det har medlemmer!"
    
    # Slett teamet
    team.delete()
    #print(f"Team {team_navn} er slettet.")
    return "Team slettet!"

@anvil.server.callable
def lagre_konkurranse(konkurransenavn, fradato, tildato):
    print(f'Lagrer konkurranse: {konkurransenavn}, {fradato}, {tildato}')
    
    # Sjekk om konkurransen allerede finnes
    konkurranse_record = app_tables.konkurranse.get(record=1)
    
    if konkurranse_record:
        # Oppdater eksisterende rekord
        konkurranse_record.update(
            konkurransenavn=konkurransenavn,
            fradato=fradato,
            tildato=tildato
        )
        #print("Eksisterende konkurranse oppdatert.")
    else:
        # Opprett ny rekord
        app_tables.konkurranse.add_row(
            record=1,
            konkurransenavn=konkurransenavn,
            fradato=fradato,
            tildato=tildato
        )
        #print("Ny konkurranse opprettet.")
    
    return "Konkurranse lagret!"

@anvil.server.callable
def delete_user_by_email(email):
    print('delete_user_by_email')
    """Sletter en bruker og alle tilhørende data basert på e-postadresse."""
    
    # Finn brukeren i users-tabellen basert på e-post
    user = app_tables.users.get(email=email)
    if not user:
        raise ValueError(f"Ingen bruker funnet med e-post: {email}")
    
    # Slett alle aktiviteter tilknyttet brukeren
    activities = app_tables.aktivitet.search(deltager=user)
    for activity in activities:
        activity.delete()
    
    # Slett brukerinfo
    user_info = app_tables.userinfo.get(user=user)
    if user_info:
        user_info.delete()
    
    # Slett selve brukeren
    user.delete()
    
    return f"Bruker med e-post {email} og tilhørende data er slettet."


@anvil.server.callable
def update_user_team(email, team_name,admin):
    print('update_user_team')
    """Oppdaterer en brukers team i userinfo-tabellen eller fjerner teamet hvis team_name er tomt."""

    # Finn brukeren basert på e-post
    user = app_tables.users.get(email=email)
    if not user:
        raise ValueError(f"Ingen bruker funnet med e-post: {email}")
    
    # Finn eller opprett brukerens info-post i userinfo-tabellen
    user_info = app_tables.userinfo.get(user=user)

    if team_name:  # Hvis team_name er oppgitt, sett brukeren til dette teamet
        team = app_tables.team.get(team=team_name)
        if not team:
            raise ValueError(f"Ingen team funnet med navn: {team_name}")
        
        if user_info:
            user_info['team'] = team  # Oppdater teamet i eksisterende userinfo
            user_info['admin'] = admin
        else:
            app_tables.userinfo.add_row(user=user, team=team, admin=admin)  # Opprett ny userinfo med team

    else:  # Hvis team_name er tomt, fjern brukeren fra teamet (hvis userinfo eksisterer)
        if user_info:
            user_info['team'] = None
            user_info['admin'] = admin

    return f"Bruker {email} er nå i team '{team_name}'" if team_name else f"Bruker {email} er fjernet fra team."

# @anvil.server.callable
# def is_admin():
#     print('is_admin')
#     user = anvil.users.get_user()
#     if user is None:
#         return False
    
#     # Slå opp brukerens info i userinfo-tabellen
#     userinfo = app_tables.userinfo.get(user=user)
#     if userinfo and userinfo['admin'] :
#         return True
#     return False

@anvil.server.callable
def oppdater_brukernavn_og_team(navn, team_streng):
    print('oppdater_brukernavn_og_team')
    bruker = anvil.users.get_user()
    if not bruker:
        raise Exception("Ingen bruker er logget inn.")

    # Finn raden i UserInfo for denne brukeren
    row = app_tables.userinfo.get(user=bruker)
    if not row:
        # Opprett ny rad hvis den ikke finnes
        row = app_tables.userinfo.add_row(user=bruker)

    # Oppdater verdier
    row['navn'] = navn
    row['team'] = app_tables.team.get(team=team_streng)
   
      

    return "OK"

@anvil.server.callable
def oppdater_team_lock(team_navn, lock_status):
    print('oppdater_team_lock')
    team_rad = app_tables.team.get(team=team_navn)
    if team_rad:
        team_rad['lock'] = lock_status
        return f"✅ Team '{team_navn}' ble oppdatert med lock={lock_status}"
    else:
        return f"❌ Fant ikke team med navn '{team_navn}'"

@anvil.server.callable
def lagre_week_offset(offset):
    print('server lagrer offset:', offset)
    user = anvil.users.get_user()
    if not user:
        raise Exception("Ingen bruker er logget inn.")

    userinfo = app_tables.userinfo.get(user=user)
    if userinfo:
        print('lagrer')
        userinfo['week_offset'] = offset
    else:
        app_tables.userinfo.add_row(user=user, week_offset=offset)

@anvil.server.callable
def slett_tomme_team():
    print('slett_tomme_team')
    for lag in app_tables.team.search():
        # Finn brukere som tilhører dette laget
        medlemmer = app_tables.userinfo.search(team=lag)
        
        if len(medlemmer) == 0:
            print(f"Sletter tomt lag: {lag['team']}")
            anvil.server.call('slett_team',lag['team'])

@anvil.server.callable
def laas_eget_team():
    print('laas_eget_team')
    user = anvil.users.get_user()
    if not user:
        return "Du må være logget inn."

    userinfo = app_tables.userinfo.get(user=user)
    if not userinfo or not userinfo['team']:
        return "Du er ikke medlem av noe team."

    team = userinfo['team']

    if team['lock']:
        return f"Teamet '{team['team']}' er allerede låst."

    # Tell hvor mange medlemmer teamet har
    medlemmer = app_tables.userinfo.search(team=team)
    antall_medlemmer = len(list(medlemmer))

    if antall_medlemmer < 3:
        return f"Teamet '{team['team']}' har bare {antall_medlemmer} medlem(mer). Minst 3 kreves for å låse."

    # Lås teamet
    team['lock'] = True
    return f"Teamet '{team['team']}' er nå låst for påmeldinger."


@anvil.server.callable
def hent_user_fra_email(email):
    print('hent_user_fra_email')
    bruker = app_tables.users.get(email=email)
    if not bruker:
        raise Exception(f"Ingen bruker funnet med e-post: {email}")
    return bruker

# ----- Plasser denne koden i en Server Module (f.eks. ServerModule1.py) -----


@anvil.server.callable
def lag_status_for_bruker():
    bruker = anvil.users.get_user()
    if not bruker:
        return "Ingen bruker logget inn."

    # Hent brukernavn og lag
    userinfo = app_tables.userinfo.get(user=bruker)
    navn = userinfo['navn'] if userinfo else bruker['email']
    plassering = userinfo['plassering']
    plassering_i_team = userinfo['team_plassering']
    
    lag_obj = userinfo['team'] if userinfo else None
    lag_navn = lag_obj['team'] if lag_obj else "Ingen lag"

    # Hent konkurransen
    konkurranse = app_tables.konkurranse.get()
    startdato = konkurranse['fradato']
    slutt_dato = konkurranse['tildato']
    
    idag = datetime.date.today()
    antall_uker = ((slutt_dato - startdato).days + 1) // 7
    nåværende_uke = ((idag - startdato).days) // 7 + 1

    statuslinjer = []

    for uke_nr in range(1, nåværende_uke + 1):
        uke_start = startdato + datetime.timedelta(days=(uke_nr - 1) * 7)
        uke_slutt = uke_start + datetime.timedelta(days=6)
        
        rader = app_tables.aktivitet.search(deltager=bruker,
                                            dato=q.between(uke_start, uke_slutt))
        
        aktiviteter = [rad['aktivitet'] for rad in rader]
        beskrivelser = [rad['beskrivelse'] for rad in rader if rad['beskrivelse']]
        total_poeng = sum(rad['poeng'] for rad in rader)

        aktiviteter_tekst = ", ".join(a for a in aktiviteter if a) if aktiviteter else "ingen"
        beskrivelse_tekst = "; ".join(beskrivelser) if beskrivelser else ""

        statuslinjer.append(f"uke {uke_nr}: {aktiviteter_tekst} (poeng: {total_poeng})")
        if beskrivelse_tekst:
            statuslinjer.append(f"beskrivelser uke {uke_nr}: {beskrivelse_tekst}")        
          
        antall_deltagere = len(app_tables.userinfo.search())
        
        plassering_tekst = f"\nplassering totalt: {plassering} av {antall_deltagere}" if plassering else "\nplassering ikke funnet"
        
        team_record = app_tables.team.get(team=lag_navn)
        lag_plassering = team_record['plassering']
        
        antall_lag = len(app_tables.team.search())
    
        lag_tekst = f"\nlag: {lag_navn} (Lagets plassering: {lag_plassering} av {antall_lag} lag)" if lag_navn != "Ingen lag" else ""
    
        # 👇 Dette er nytt
        team_plassering_tekst = f"\nplassering innenfor eget lag: {plassering_i_team}" if plassering_i_team else "\nplassering i laget ikke tilgjengelig"
    
        # Sett sammen alt – og fiks join-feil
        status = f"navn: {navn}{plassering_tekst}{lag_tekst}{team_plassering_tekst}\n" + "\n".join(statuslinjer)
    
        return status



# @anvil.server.callable
# def lag_status_for_bruker():
#     print('lag_status_for_bruker')
#     bruker = anvil.users.get_user()
#     if not bruker:
#         return "Ingen bruker logget inn."

#     # Hent brukernavn og lag
#     userinfo = app_tables.userinfo.get(user=bruker)
#     navn = userinfo['navn'] if userinfo else bruker['email']
#     lag_obj = userinfo['team'] if userinfo else None
#     lag_navn = lag_obj['team'] if lag_obj else "Ingen lag"

#     # Hent konkurransen
#     konkurranse = app_tables.konkurranse.get()
#     startdato = konkurranse['fradato']
#     slutt_dato = konkurranse['tildato']
    
#     idag = datetime.date.today()
#     antall_uker = ((slutt_dato - startdato).days + 1) // 7
#     nåværende_uke = ((idag - startdato).days) // 7 + 1

#     statuslinjer = []

#     for uke_nr in range(1, nåværende_uke + 1):
#         uke_start = startdato + datetime.timedelta(days=(uke_nr - 1) * 7)
#         uke_slutt = uke_start + datetime.timedelta(days=6)
        
#         rader = app_tables.aktivitet.search(deltager=bruker,
#                                             dato=q.between(uke_start, uke_slutt))
        
#         aktiviteter = [rad['aktivitet'] for rad in rader]
#         beskrivelser = [rad['beskrivelse'] for rad in rader if rad['beskrivelse']]
#         total_poeng = sum(rad['poeng'] for rad in rader)

#         aktiviteter_tekst = ", ".join(a for a in aktiviteter if a) if aktiviteter else "ingen"
#         beskrivelse_tekst = "; ".join(beskrivelser) if beskrivelser else ""

#         statuslinjer.append(f"uke {uke_nr}: {aktiviteter_tekst} (poeng: {total_poeng})")
#         if beskrivelse_tekst:
#             statuslinjer.append(f"beskrivelser uke {uke_nr}: {beskrivelse_tekst}")
    
    
#     # Finn brukerens plassering basert på ny score
#     alle_poeng = hent_poengsummer()
    
#     # Beregn score for hver bruker
#     for d in alle_poeng:
#         d["score"] = (100 * (d.get("poeng", 0) + d.get("bonus", 0))) + d.get("longest_streak", 0)
    
#     # Sorter etter score, høyest først
#     alle_poeng.sort(key=lambda d: d["score"], reverse=True)
    
#     # Finn brukerens plassering
#     plassering = next((i + 1 for i, d in enumerate(alle_poeng) if d["email"] == bruker["email"]), None)
#     plassering_tekst = f"\nplassering totalt: {plassering} av {len(alle_poeng)}" if plassering else "\nplassering ikke funnet"

#     # Finn lagets plassering
#     lag_resultater = hent_team_poengsummer()
#     lag_plassering = next((i + 1 for i, d in enumerate(lag_resultater) if d["team"] == lag_navn), None)
#     lag_tekst = f"\nlag: {lag_navn} (plassering: {lag_plassering} av {len(lag_resultater)})" if lag_navn != "Ingen lag" else ""

#     # Sett sammen alt
#     status = f"navn: {navn}{plassering_tekst}{lag_tekst}\n" + "\n".join(statuslinjer)
#     return status

@anvil.server.callable
def beregn_plassering(email):
    print('beregn_plassering')
    alle_poeng = hent_poengsummer()

    for d in alle_poeng:
        d["score"] = (100 * (d.get("poeng", 0) + d.get("bonus", 0))) + d.get("longest_streak", 0)

    alle_poeng.sort(key=lambda d: d["score"], reverse=True)

    plassering = next((i + 1 for i, d in enumerate(alle_poeng) if d["email"] == email), None)
    return {
        "plassering": plassering,
        "antall_deltakere": len(alle_poeng)
    }

@anvil.server.callable
def generer_oppmuntring_for_bruker():
    print('generer_oppmuntring_for_bruker')
    import random
    bruker = anvil.users.get_user()
    if not bruker:
        return "Fant ikke innlogget bruker."

    # Hent status-tekst
    status = lag_status_for_bruker()
    print(status)
     
    # Hent alle tilgjengelige prompts fra databasen
    alle_prompter = list(app_tables.ai_prompt.search())
    if not alle_prompter:
        return "Ingen AI-prompter funnet i tabellen."

    # Velg én tilfeldig prompt
    valgt_prompt_mal = random.choice(alle_prompter)['prompt']

    # Sett inn status i prompten
    if "{status}" in valgt_prompt_mal:
        prompt = valgt_prompt_mal.replace("{status}", status)
    else:
        prompt = f"{valgt_prompt_mal}\n\nStatus:\n{status}"

    # Sett OpenAI-nøkkel
    openai.api_key = get_secret("openai_key")

    try:
        # Send forespørsel til OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du er en positiv, humoristisk treningscoach for en aktivitetskonkurranse på jobb."},
                {"role": "system", "content": "Du representerer bedriftsidrettslaget, Framo BIL. Ikke bruk noen tittel på deg selv. Bruk gjerne fornavn til deltageren. "},
                {"role": "user", "content": " I konkurransen må man gå få poeng fem dager i uken for å delta i ukentlig trekning av store premier. Pengene er en motiverende faktor for deltagerne. "},
              
                {"role": "user", "content": "Det er også en lagkonkurranse, for de som er med på et lag. For alle er det en indibviduell konkurranse, men det viktigste er at de får en vane med å trene litt hver dag"},
                {"role": "user", "content": "Ikke avslutt med et spørsmål."},
                {"role": "user", "content": "Konkurransen går over 10 uker"},
          
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=300
        )

        melding = response.choices[0].message.content.strip()
        
        return melding

    except Exception as e:
        return f"Feil ved henting av AI-melding: {e}"


@anvil.server.callable
def hent_prompter():
    return list(app_tables.ai_prompt.search())

@anvil.server.callable
def lagre_prompt(prompt_rad, ny_tekst):
    if prompt_rad and ny_tekst:
        prompt_rad['prompt'] = ny_tekst
        return "Prompt oppdatert"
    else:
        return "Mangler data – kunne ikke oppdatere"

@anvil.server.callable
def legg_til_prompt(prompt_tekst):
    #if not prompt_tekst or "{status}" not in prompt_tekst:
    #    return "Prompt må inneholde teksten {status} for å fungere."

    app_tables.ai_prompt.add_row(prompt=prompt_tekst)
    return "Prompt lagt til!"



# @anvil.server.background_task
# def nightly_streak_recalc():
#     anvil.server.call('tildel_badges_for_alle_brukere')
#     anvil.server.call('oppdater_poeng_og_score_for_alle')
#     anvil.server.call('oppdater_team_poengsummer')
#     anvil.server.call('update_team_placements')
#     anvil.server.call('beregn_opprykk_og_nedrykk')

    
  



@anvil.server.callable
def nightly_streak_recalc_test():
    print('nightly_streak_recalc_test')
    nightly_streak_recalc()

@anvil.server.callable
def tildel_badges_for_alle_brukere():
    for bruker in app_tables.users.search():
        sjekk_og_tildel_badges(bruker)

# def sjekk_og_tildel_badges(bruker):
#     if sjekk_badge_1(bruker):
#         badge=1
#         tildel_badge(bruker,badge)

#     if sjekk_badge_2(bruker):
#       badge=2
#       tildel_badge(bruker,badge)

#     if sjekk_badge_3(bruker):
#       badge=3
#       tildel_badge(bruker,badge)

#     if sjekk_badge_4(bruker):
#       badge=4
#       tildel_badge(bruker,badge)

#     if sjekk_badge_5(bruker):
#       badge=5
#       tildel_badge(bruker,badge)

#     if sjekk_badge_6(bruker):
#       badge=6
#       tildel_badge(bruker,badge)
      
#     if sjekk_badge_7(bruker):
#       badge=7
#       tildel_badge(bruker,badge)

#     if sjekk_badge_8(bruker):
#       badge=8
#       tildel_badge(bruker,badge)

#     if sjekk_badge_9(bruker):
#       badge=9
#       tildel_badge(bruker,badge)

#     if sjekk_badge_10(bruker):
#       badge=10
#       tildel_badge(bruker,badge)

#     if sjekk_badge_11(bruker):
#       badge=11
#       tildel_badge(bruker,badge)

def tildel_badge(bruker, badge_id):
    badge = app_tables.badges.get(id=badge_id)
    if not badge:
        print(f"❌ Badge med id={badge_id} finnes ikke.")
        return

    if app_tables.user_badges.get(user=bruker, badge=badge):
        return

    app_tables.user_badges.add_row(
        user=bruker,
        badge=badge,
        awarded_date=datetime.datetime.now(),
        informert=False
    )
    print(f"🏅 Tildelt badge {badge['name']} til {bruker['email']}")

    userinfo = app_tables.userinfo.get(user=bruker)
    if userinfo:
        gammel_bonus = userinfo['bonus'] or 0
        ekstra_bonus = badge['bonus'] or 0
        ny_bonus = gammel_bonus + ekstra_bonus
        userinfo.update(bonus=ny_bonus)
        print(f"➕ Lagt til {ekstra_bonus} bonuspoeng (totalt: {ny_bonus})")

@anvil.server.callable
def start_badge_sjekk_manually():
    tildel_badges_for_alle_brukere()

@anvil.server.background_task
def nightly_badge_check():
    print("🌙 Starter nattlig badge-sjekk")
    tildel_badges_for_alle_brukere()
    print("🌟 Ferdig med badge-sjekk")


@anvil.server.callable
def generer_badge_melding(badge_id):
    print('generer_badge_melding')
    bruker = anvil.users.get_user()
    if not bruker:
        return "Fant ikke innlogget bruker."

    # Hent status
    status = lag_status_for_bruker()

    # Hent badge fra databasen
    badge_rad = app_tables.badges.get(id=badge_id)
    if not badge_rad:
        return f"Fant ikke badge med id {badge_id}"

    # Hent prompt
    prompt_mal = badge_rad['prompt']
    if not prompt_mal:
        return f"Badge {badge_id} har ikke noe prompt."

    # Sett sammen prompt
    if "{status}" in prompt_mal:
        prompt = prompt_mal.replace("{status}", status)
    else:
        prompt = f"{prompt_mal}\n\nStatus:\n{status}"

    # Sett OpenAI-nøkkel
    openai.api_key = get_secret("openai_key")
    print(prompt)
    try:
        # Send prompt til OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du er en stemmen til og treningscoach i Framo BIL sin aktivitetskonkurranse."},
                {"role": "system", "content": "Du skal informere brukeren om en badge de har vunnet, og feire det på en inspirerende måte."},
                {"role": "user", "content": "Konkurransen varer i 10 uker. Deltagerne får poeng for å være aktive, og kan vinne ulike badges basert på innsats."},
                {"role": "user", "content": "Ikke avslutt med spørsmål."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=300
        )
        
        melding = response.choices[0].message.content.strip()
        app_tables.ai_log.add_row(
            user=bruker,
            date=datetime.datetime.now(),
            prompt=prompt,
            svar=melding
)
        return melding

    except Exception as e:
        return f"Feil ved henting av AI-melding: {e}"


@anvil.server.callable
def sett_skritt_first(verdi: bool):
    print('sett_skritt_first')
    from anvil.tables import app_tables
    user = anvil.users.get_user()
    userinfo_rad = app_tables.userinfo.get(user=user)

    if userinfo_rad:
        userinfo_rad["skritt_first"] = verdi
    else:
        app_tables.userinfo.add_row(user=user, skritt_first=verdi)

@anvil.server.callable
def toggle_korrigering():
    konkurranse = app_tables.konkurranse.search()[0]  # Antar kun én record
    if konkurranse:
        ny_verdi = not konkurranse['korrigering']
        konkurranse['korrigering'] = ny_verdi
        return ny_verdi  # Returnerer ny verdi etter toggle
    else:
        raise Exception("Fant ingen konkurranse-record.")

@anvil.server.callable
def hent_ai_log():
    rader = app_tables.ai_log.search(tables.order_by("date", ascending=False))
    resultat = []

    for rad in rader:
        user_rad = rad['user']
        email = user_rad['email'] if user_rad else "Ukjent"

        resultat.append({
            "email": email,
            "prompt": rad['prompt'],
            "svar": rad['svar'],
            "dato": rad['date']
        })

    return resultat

# Server Module


@anvil.server.callable
def lagre_ny_aktivitet(aktivitet_tekst: str):

    bruker = anvil.users.get_user()
    if not bruker:
        raise Exception("Bruker ikke innlogget")

    app_tables.ny_aktivitet.add_row(
        user=bruker,
        dato=datetime.datetime.now(),
        aktivitet=aktivitet_tekst,
        behandlet=False
    )
    anvil.server.call('send_email',"qf@simba.no", "forslag om ny idrett", aktivitet_tekst)


@anvil.server.callable
def toggle_ny_aktivitet(rad):
    if not rad:
        raise ValueError("Ingen rad ble sendt inn")

    ny_verdi = not rad['behandlet']
    rad['behandlet'] = ny_verdi
    return ny_verdi

@anvil.server.callable
def send_email(to,subject,html):
    print(f"mailer to: {to} subject: {subject} html: {html}")
    anvil.email.send(
    from_address="support@framskritt.framo.com",
    from_name="Framskritt Support",
    subject=subject,
    html=html
  )

def sjekk_badge_1(bruker):
    # streak > 3
    userinfo = app_tables.userinfo.get(user=bruker)
    return userinfo and userinfo['longest_streak'] >= 3

def sjekk_badge_2(bruker):
    #streak > 7
    userinfo = app_tables.userinfo.get(user=bruker)
    return userinfo and userinfo['longest_streak'] >= 7

def sjekk_badge_3(bruker):
    #Triathlon
    aktiviteter = app_tables.aktivitet.search(deltager=bruker)

    ikoner = {akt['ikon'] for akt in aktiviteter if akt['ikon']}

    har_sykkel = 'sykling' in ikoner
    har_svømming = 'svømming' in ikoner
    har_lop = 'løp' in ikoner

    return har_sykkel and har_svømming and har_lop

def sjekk_badge_4(bruker):
    # 8 like treninger
    # Hent alle aktiviteter for brukeren
    aktiviteter = app_tables.aktivitet.search(deltager=bruker)

    # Tell forekomster av hver aktivitetstype (ikon)
    ikon_teller = {}

    for akt in aktiviteter:
        ikon = akt['aktivitet']
        if ikon and "Skritt" not in ikon:
            ikon_teller[ikon] = ikon_teller.get(ikon, 0) + 1

    # Sjekk om noen aktivitetstyper har 8 eller flere forekomster
    print(ikon_teller)
    for antall in ikon_teller.values():
        if antall >= 8:
            return True

    return False

def sjekk_badge_5(bruker):
    # 24 like treninger
    # Hent alle aktiviteter for brukeren
    aktiviteter = app_tables.aktivitet.search(deltager=bruker)

    # Tell forekomster av hver aktivitetstype (ikon)
    ikon_teller = {}

    for akt in aktiviteter:
        ikon = akt['aktivitet']
        if ikon and "Skritt" not in ikon:
            ikon_teller[ikon] = ikon_teller.get(ikon, 0) + 1

    # Sjekk om noen aktivitetstyper har 8 eller flere forekomster
    for antall in ikon_teller.values():
        if antall >= 24:
            return True

    return False

def sjekk_badge_6(bruker):
    from datetime import timedelta

    aktiviteter = app_tables.aktivitet.search(deltager=bruker)
    helgepoeng = {}

    for akt in aktiviteter:
        dato = akt['dato']

        try:
            poeng = akt['poeng']
        except KeyError:
            poeng = 0

        if poeng is None:
            poeng = 0

        if not dato:
            continue

        ukedag = dato.weekday()  # 0 = mandag, 6 = søndag



        if ukedag in [4, 5, 6]:  # fredag–søndag
            antall_dager_tilbake = ukedag - 4
            fredag_dato = dato - timedelta(days=antall_dager_tilbake)

            #print(f"{bruker['email']}, {akt['aktivitet']}, {poeng} poeng, dato: {dato}")

            helgepoeng[fredag_dato] = helgepoeng.get(fredag_dato, 0) + poeng

    for fredag, poengsum in helgepoeng.items():
        #print(f"Helg som starter {fredag}: {poengsum} poeng")
        if poengsum >= 9:
            return True

    return False

def sjekk_badge_7(bruker):
    from datetime import date
    today = date.today()
    if today.weekday() != 4:  # 0 = mandag, 4 = fredag
        return False
    userinfo = app_tables.userinfo.get(user=bruker)
    if not userinfo:
        return False
    plassering = userinfo['plassering']
    if plassering == 1:
        return True
    return False

def sjekk_badge_8(bruker):
    from datetime import date
    today = date.today()
    if today.weekday() != 4:  # 0 = mandag, 4 = fredag
        return False
    userinfo = app_tables.userinfo.get(user=bruker)
    if not userinfo:
        return False
    plassering = userinfo['plassering']
    if plassering == 2:
        return True
    return False

def sjekk_badge_9(bruker):
    from datetime import date
    today = date.today()
    if today.weekday() != 4:  # 0 = mandag, 4 = fredag
        return False
    userinfo = app_tables.userinfo.get(user=bruker)
    if not userinfo:
        return False
    plassering = userinfo['plassering']
    if plassering == 3:
        return True
    return False



def sjekk_badge_10(bruker):
    
    today = date.today()
    if today.weekday() != 6:  # 6 = søndag, 2 = onsdag for testing    
        return False
    userinfo = app_tables.userinfo.get(user=bruker)
    if not userinfo:    
        return False
    lag = userinfo['team']
    if not lag:    
        return False
    # Bruk get_id() for å sammenligne lag
    lag_id = lag.get_id()
    medlemmer = [m for m in app_tables.userinfo.search() if m['team'] and m['team'].get_id() == lag_id]
    
    
    if len(medlemmer) < 3:    
        return False

    topp_plassering = [m for m in medlemmer if m['team_plassering'] == 1]
    print(f"Antall med 1. plass: {len(topp_plassering)}")
    for m in topp_plassering:
        print(f"1.plass bruker: {m['user']['email']}")

    bruker_epost = bruker['email']
    brukere_med_epost = [m['user']['email'] for m in topp_plassering]

    if brukere_med_epost.count(bruker_epost) == 1 and len(topp_plassering) == 1:
        print('bingo')
        return True

    print('end of routine')
    return False

def sjekk_badge_11(bruker): #Comeback


    # Hent alle datoer med poeng for brukeren, sortert stigende
    aktivitetsdatoer = sorted([
        rad['dato'] for rad in app_tables.aktivitet.search(deltager=bruker)
        if rad['poeng'] and rad['dato']
    ])

    if len(aktivitetsdatoer) < 2:
        # Må ha minst én pause etter tidligere aktivitet
        return False

    # Gå gjennom datoene og se om det finnes en pause på minst 3 dager
    for i in range(1, len(aktivitetsdatoer)):
        forrige = aktivitetsdatoer[i - 1]
        nåværende = aktivitetsdatoer[i]
        if (nåværende - forrige).days >= 3:
            return True  # Fant et comeback!

    return False





@anvil.server.callable
def beregn_bonus_fra_badges_og_ligaopprykk():
    print('🔄 Beregner bonus fra badges + ligaopprykk...')
    from collections import defaultdict

    # 1. Samle badge-bonus per bruker
    badge_bonus_per_user = defaultdict(int)
    for rad in app_tables.user_badges.search():
        bruker = rad['user']
        badge = rad['badge']
        if bruker and badge:
            badge_bonus = badge['bonus'] or 0
            badge_bonus_per_user[bruker] += badge_bonus

    # 2. Samle opprykksbonus per bruker
    liga_bonus_per_user = defaultdict(int)
    for row in app_tables.liga_opprykk_bonus.search():
        bruker = row['user']
        bonus = row['opprykk_bonus'] or 0
        liga_bonus_per_user[bruker] += bonus

    # 3. Summer og oppdater total bonus i userinfo
    for bruker in app_tables.users.search():
        userinfo = app_tables.userinfo.get(user=bruker)
        if not userinfo:
            continue

        badge_bonus = badge_bonus_per_user.get(bruker, 0)
        liga_bonus = liga_bonus_per_user.get(bruker, 0)
        total_bonus = badge_bonus + liga_bonus

        userinfo['bonus'] = total_bonus
        print(f"🎯 {bruker['email']} – badge: {badge_bonus}, liga: {liga_bonus}, total: {total_bonus}")


@anvil.server.callable
def oppdater_team_poengsummer():
    # Lag en mapping fra team til medlemmer
    team_medlemmer = {}

    for userinfo in app_tables.userinfo.search():
        team = userinfo['team']
        if team:
            if team not in team_medlemmer:
                team_medlemmer[team] = []
            team_medlemmer[team].append(userinfo)

    # Oppdater hvert team
    for team, medlemmer in team_medlemmer.items():
        if not medlemmer:
            continue

        total_poeng = sum(m['poeng'] or 0 for m in medlemmer)
        total_bonus = sum(m['bonus'] or 0 for m in medlemmer)
        longest_streak = max((m['longest_streak'] or 0) for m in medlemmer)
        antall_medlemmer = len(medlemmer)

        if antall_medlemmer < 3:
            score = 0
        else:
            score = round(((total_poeng + total_bonus) * 100 + longest_streak) / antall_medlemmer)

        # Oppdater team-raden med alle verdier, inkludert members
        team.update(
            poeng=total_poeng,
            bonus=total_bonus,
            longest_streak=longest_streak,
            score=score,
            members=antall_medlemmer
        )

    # --- NY DEL: Sett plassering basert på score ---
    team_list = list(app_tables.team.search())
    team_list.sort(key=lambda t: t['score'] or 0, reverse=True)

    plassering = 1
    for idx, team in enumerate(team_list):
        if idx == 0:
            current_rank = plassering
        else:
            previous_team = team_list[idx - 1]
            if team['score'] == previous_team['score']:
                # Samme score = delt plassering
                pass
            else:
                plassering = idx + 1
            current_rank = plassering

        team.update(plassering=current_rank)

    return "Team-poengsummer, medlemstall og plasseringer oppdatert!"

@anvil.server.callable
def update_badge(item):
    badge_id = item['id']  # <-- bruker [] ikke .get()
    if not badge_id:
        raise ValueError("Item must contain an 'id' field.")
    
    # Finn eksisterende badge med riktig id
    badges = app_tables.badges.search(id=badge_id)
    
    if not badges:
        raise ValueError(f"No badge found with id {badge_id}")
    
    badge = badges[0]

    # Oppdater feltene
    badge['name'] = item['name']
    badge['description'] = item['description']
    badge['bonus'] = item['bonus']
    badge['prompt'] = item['prompt']

    return badge

@anvil.server.callable
def update_team_placements():
    from anvil.tables import app_tables

    all_users = list(app_tables.userinfo.search())

    # Grupper brukerne etter lag
    teams = {}
    for user in all_users:
        team = user['team']
        if team not in teams:
            teams[team] = []
        teams[team].append(user)

    # Gå gjennom hvert lag
    for team, members in teams.items():
        if len(members) < 3:
            # Mindre enn 3 medlemmer: Sett plassering 0
            for user in members:
                user['team_plassering'] = 0
            continue  # Hopp til neste lag

        # Ellers: sorter og gi vanlig plassering
        sorted_members = sorted(members, key=lambda u: u['score'] or 0, reverse=True)

        placement = 1
        previous_score = None

        for idx, user in enumerate(sorted_members, start=1):
            user_score = user['score'] or 0

            if user_score == previous_score:
                # Samme score som forrige: beholder plassering
                pass
            else:
                # Ny score: oppdater plassering
                placement = idx

            user['team_plassering'] = placement
            previous_score = user_score

@anvil.server.callable
def fordel_liga():
    
    from collections import defaultdict

    # Hent liga-rader 4 til 7
    # Hent liga-rader for level 4 til 7
    ligaer = app_tables.ligaer.search()
    liga_map = {l['level']: l for l in ligaer if l['level'] in range(4, 8)}


    # Hent alle brukere med plassering
    brukere = [b for b in app_tables.userinfo.search() if b['plassering'] is not None]

    # Grupper brukere etter plassering
    grupper = defaultdict(list)
    for bruker in brukere:
        grupper[bruker['plassering']].append(bruker)

    # Sorter plasseringer stigende
    sorterte_plasseringer = sorted(grupper.keys())

    total = len(brukere)
    kvote = total / 4
    tildelt = 0
    liga_index = 0
    liga_nivåer = [4, 5, 6, 7]

    print(f"Totalt {total} brukere – ca {kvote:.1f} per liga")

    # Fordel gruppevis etter plassering
    for plassering in sorterte_plasseringer:
        gruppe = grupper[plassering]

        if liga_index >= len(liga_nivåer):
            print("Alle ligaer fylt – resten legges i siste liga")
            liga_index = len(liga_nivåer) - 1

        current_liga = liga_map[liga_nivåer[liga_index]]

        for bruker in gruppe:
            bruker['liga'] = current_liga

        tildelt += len(gruppe)
        print(f"Tildelt {len(gruppe)} brukere med plassering {plassering} til {current_liga['liga']}")

        if tildelt >= (liga_index + 1) * kvote:
            liga_index += 1

    print("Liga-fordeling fullført.")

@anvil.server.callable
def beregn_opprykk_og_nedrykk():
    # Tøm tidligere rader
    for rad in app_tables.liga_opprykk.search():
        rad.delete()

    # Hent ligaer sortert fra dårligst til best
    ligaer = sorted(app_tables.ligaer.search(), key=lambda l: l['level'])

    max_level = max(l['level'] for l in ligaer)
    min_level = min(l['level'] for l in ligaer)
    print('a')
    for liga in ligaer:
        print('b')
        brukere_i_liga = [u for u in app_tables.userinfo.search() if u['liga'] == liga]
        antall = len(brukere_i_liga)
        if antall < 2:
            continue

        brukere_i_liga.sort(key=lambda u: u['plassering'])

        antall_opprykk = max(1, round(antall * 0.2))
        antall_nedrykk = max(1, round(antall * 0.2))

        if liga['level'] == max_level:
            antall_opprykk = 0
        if liga['level'] == min_level:
            antall_nedrykk = 0

      
        # Emoji-mapping
        symboler = {'up': '⬆️', 'same': '➡️', 'down': '⬇️'}
        print('c')
        for bruker in brukere_i_liga[:antall_opprykk]:
            print('d')
            users_record = bruker['user']
            #print('navn ',brukere_i_liga['navn'])
            #print('email ',users_record['email'])
            print('e')
            #bruker_user = bruker['user']
            bruker_user = users_record
            print('f')
            if not bruker_user:
                continue
            app_tables.liga_opprykk.add_row(
                user=bruker_user, liga=liga, status='up', opprykk=symboler['up'], notified=False
            )
        
        for bruker in brukere_i_liga[-antall_nedrykk:]:
            bruker_user = bruker['user']
            if not bruker_user:
                continue
            app_tables.liga_opprykk.add_row(
                user=bruker_user, liga=liga, status='down', opprykk=symboler['down'], notified=False
            )
        
        for bruker in brukere_i_liga[antall_opprykk:-antall_nedrykk]:
            bruker_user = bruker['user']
            if not bruker_user:
                continue
            app_tables.liga_opprykk.add_row(
                user=bruker_user, liga=liga, status='same', opprykk=symboler['same'], notified=False
            )

      
# Optimalisert nightly_streak_recalc med cache og logging
@anvil.server.callable
def nightly_streak_recalc():
    print("\n🌙 Starter optimalisert nattkjøring...")
    start_total = time.time()

    # 1. Hent alle nødvendige rader
    user_rows = [u for u in app_tables.users.search() if u is not None]
    userinfo_rows = list(app_tables.userinfo.search())
    aktivitet_rows = list(app_tables.aktivitet.search())
    user_badges_rows = list(app_tables.user_badges.search())
    badges_rows = list(app_tables.badges.search())

    # 2. Lag oppslag for aktiviteter og badge-bonus
    aktivitet_per_user = defaultdict(list)
    for a in aktivitet_rows:
        deltager = a['deltager']
        if deltager:
            aktivitet_per_user[deltager].append(a)

    badge_bonus_map = {}
    for b in badges_rows:
        badge_id = b['id'] if 'id' in b else None
        if badge_id is not None:
            badge_bonus_map[badge_id] = b['bonus'] or 0

    bonus_per_user = defaultdict(int)
    for row in user_badges_rows:
        try:
            bruker = row['user'] if 'user' in row else None
            badge = row['badge'] if 'badge' in row else None
            if not (bruker and badge and 'id' in badge):
                continue
            badge_id = badge['id']
            bonus_per_user[bruker] += badge_bonus_map.get(badge_id, 0)
        except Exception as e:
            print(f"⚠️ Feil i bonus-loop: {e}")

    userinfo_per_user = {r['user']: r for r in userinfo_rows if r['user'] is not None}

    # 3. Tildel badges
    print("🏅 Tildeler badges...")
    for bruker in user_rows:
        aktiviteter = aktivitet_per_user.get(bruker, [])
        userinfo = userinfo_per_user.get(bruker)
        if userinfo:
            sjekk_og_tildel_badges_optimalisert(bruker, userinfo, aktiviteter)
            print('returnert fra sjekk badges')

    # 4. Beregn poeng og score
    print("📊 Oppdaterer score...")
    today = date.today()

    for bruker in user_rows:
        userinfo = userinfo_per_user.get(bruker)
        if not userinfo:
            print('not userinfo')
            continue
        #print(userinfo['navn'])
        aktiviteter = aktivitet_per_user.get(bruker, [])
        total_poeng = sum(a['poeng'] or 0 for a in aktiviteter if a['dato'] and a['dato'] < today)
        longest_streak = calculate_longest_streak_from_aktiviteter(aktiviteter)
        bonus = userinfo['bonus']
        print('tot',total_poeng,bonus,)
        score = ((total_poeng + bonus) * 100) + longest_streak
        userinfo.update(poeng=total_poeng, longest_streak=longest_streak, bonus=bonus, score=score)

    # 5. Sett plasseringer
    brukere_med_score = [u for u in userinfo_rows if u['score'] is not None]
    brukere_med_score.sort(key=lambda u: u['score'], reverse=True)
    plassering = 1
    for idx, userinfo in enumerate(brukere_med_score):
        if idx > 0 and userinfo['score'] != brukere_med_score[idx - 1]['score']:
            plassering = idx + 1
        userinfo['plassering'] = plassering

    # 6. Oppdater lag og liga
    print("➡️ Kaller oppdater_team_poengsummer")
    anvil.server.call('oppdater_team_poengsummer')

    print("➡️ Kaller beregn bonus fra badges og ligaopprykk")
    anvil.server.call('beregn_bonus_fra_badges_og_ligaopprykk')
    
    print("➡️ Kaller update_team_placements")
    anvil.server.call('update_team_placements')
    
    print("➡️ Kaller beregn_opprykk_og_nedrykk")
    anvil.server.call('beregn_opprykk_og_nedrykk')

    print(f"✅ Nattkjøring ferdig på {time.time() - start_total:.2f} sekunder.")



def sjekk_og_tildel_badges_optimalisert(bruker, userinfo, aktiviteter):
    if not bruker or not userinfo:
        return
    print('sjekk badge1')
    if sjekk_badge_1(bruker): tildel_badge(bruker, 1)
    print('sjekk badge2')
    if sjekk_badge_2(bruker): tildel_badge(bruker, 2)
    print('sjekk badge3')
    if sjekk_badge_3(aktiviteter): tildel_badge(bruker, 3)
    print('sjekk badge4')
    if sjekk_badge_4(aktiviteter): tildel_badge(bruker, 4)
    print('sjekk badge5')  
    if sjekk_badge_5(aktiviteter): tildel_badge(bruker, 5)
    print('sjekk badge6')
    if sjekk_badge_6(aktiviteter): tildel_badge(bruker, 6)


def sjekk_badge_3(aktiviteter):
    ikoner = {akt['ikon'] for akt in aktiviteter if akt['ikon']}
    return 'sykling' in ikoner and 'svømming' in ikoner and 'løp' in ikoner


def sjekk_badge_4(aktiviteter):
    teller = defaultdict(int)
    for akt in aktiviteter:
        navn = akt['aktivitet']
        if navn and "Skritt" not in navn:
            teller[navn] += 1
    return any(antall >= 8 for antall in teller.values())


def sjekk_badge_5(aktiviteter):
    teller = defaultdict(int)
    for akt in aktiviteter:
        navn = akt['aktivitet']
        if navn and "Skritt" not in navn:
            teller[navn] += 1
    return any(antall >= 24 for antall in teller.values())


def sjekk_badge_6(aktiviteter):
    helgepoeng = defaultdict(int)
    for akt in aktiviteter:
        dato = akt['dato']
        poeng = akt['poeng'] if 'poeng' in akt else 0
        if dato and dato.weekday() in [4, 5, 6]:
            fredag = dato - timedelta(days=dato.weekday() - 4)
            helgepoeng[fredag] += poeng
    return any(poengsum >= 9 for poengsum in helgepoeng.values())


def calculate_longest_streak_from_aktiviteter(aktiviteter):
    today = date.today()
    aktive_dager = sorted(
        {a['dato'] for a in aktiviteter if (a['poeng'] or 0) > 0 and a['dato'] and a['dato'] < today},
        reverse=True
    )
    if not aktive_dager:
        return 0

    longest = current = 0
    prev_day = None

    for d in aktive_dager:
        if prev_day is None or (prev_day - d).days == 1:
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        prev_day = d
    
    return longest



@anvil.server.callable
def gjennomfor_ligabyttene():
    ligaer = sorted(app_tables.ligaer.search(), key=lambda l: l['level'])  # 1 = lavest, 10 = høyest
    liga_nivåer = {liga['level']: liga for liga in ligaer}
    max_level = max(liga_nivåer.keys())
    now = datetime.datetime.now()

    for rad in app_tables.liga_opprykk.search():
        users_rad = rad['user']
        userinfo_rad = app_tables.userinfo.get(user=users_rad)
        
        nåværende_liga = userinfo_rad['liga']
        status = rad['status']

        if not userinfo_rad or not nåværende_liga:
            continue

        if status != "up":
            continue  # Ignorer "same" og "down"

        nåværende_level = nåværende_liga['level']
        
        # Beregn ny liga (selv om det kan være samme)
        if nåværende_level < max_level:
            ny_liga = liga_nivåer[nåværende_level + 1]
        else:
            ny_liga = nåværende_liga  # Allerede i topp-liga

        # Oppdater brukerens liga uansett
        userinfo_rad['liga'] = ny_liga

        # Legg inn bonus og flytteinfo
        app_tables.liga_opprykk_bonus.add_row(
            user=userinfo_rad['user'],
            opprykk_bonus=2,
            informert=False,
            til_liga=ny_liga,
            status="up",
            date=now
        )


@anvil.server.callable
def generer_opprykk_melding(bruker,til_liga):
    print('generer_opprykk_melding')
    bruker = anvil.users.get_user()
    if not bruker:
        return "Fant ikke innlogget bruker."
    opprykk=app_tables.liga_opprykk_bonus.get(user=bruker, til_liga=til_liga)
    if opprykk:
      # Hent status
        status = lag_status_for_bruker()
        # Hent prompt
        prompt_mal = f"Nå skal du informere deltageren om at hen har oppnådd opprykk til en bedre liga. Den nye ligaen heter {til_liga}. Dette utløser {opprykk[opprykk_bonus]} bonuspoeng. Samtidig kan du kikke på aktivitene deltageren har gjort i stsus som følger, og skryte av de."

        prompt = f"{prompt_mal}\n\nStatus:\n{status}" 

        # Sett OpenAI-nøkkel
        openai.api_key = get_secret("openai_key")
        print(prompt)
        try:
            # Send prompt til OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Du er en stemmen til og treningscoach i Framo BIL sin aktivitetskonkurranse."},
                    {"role": "system", "content": "Du skal informere brukeren om opprykk i ny og bedre liga og feire det på en inspirerende måte."},
                    {"role": "user", "content": "Konkurransen varer i 10 uker. Deltagerne får poeng for å være aktive, og kan vinne ulike badges basert på innsats. De er også delt i ligaer og får bonuspoeng for å flyttes i bedsre liga."},
                    {"role": "user", "content": "Ikke avslutt med spørsmål."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            melding = response.choices[0].message.content.strip()
            app_tables.ai_log.add_row(
                user=bruker,
                date=datetime.datetime.now(),
                prompt=prompt,
                svar=melding              
              )
        
            return melding

        except Exception as e:
          return f"Feil ved henting av AI-melding: {e}"