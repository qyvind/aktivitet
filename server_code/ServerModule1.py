import anvil.email
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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


import anvil.server
import anvil.users

import anvil.server
import anvil.users

@anvil.server.callable
def batch_create_users(user_list):
    print('batch_create_users')

    if not isinstance(user_list, list):
        print("Feil: Forventet en liste over brukere, men fikk noe annet.")
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
                print(f"Bruker {email} finnes allerede, hopper over.")
                continue

            # Opprett ny bruker
            anvil.users.signup_with_email(email, password)
            print(f"Bruker {email} opprettet.")

            # Hent den opprettede brukeren igjen
            created_user = app_tables.users.get(email=email)
            if created_user:
                app_tables.userinfo.add_row(user=created_user, navn=navn)
                print(f"Bruker {email} opprettet med navn {navn}.")
            else:
                print(f"Kunne ikke finne brukeren {email} etter opprettelse.")

        except KeyError as e:
            print(f"Feil: Manglende nøkkel {e} i brukerdata: {user}")
        except Exception as e:
            print(f"Uventet feil for bruker {user}: {e}")

    return "Alle brukere er lagt til!"




@anvil.server.callable
def lagre_aktivitet(dato, aktivitet, poeng):
    print('lagre_aktivitet')
    user = anvil.users.get_user()
    if not user:
        raise Exception("Ingen bruker er pålogget")
    
    # Sjekk om det allerede finnes en post for den aktuelle datoen og brukeren
    existing_activity = app_tables.aktivitet.get(deltager=user, dato=dato)
    
    if existing_activity:
        # Oppdater den eksisterende posten
        existing_activity.update(aktivitet=aktivitet, poeng=poeng)
        return "Aktivitet oppdatert"
    else:
        # Lagre ny post i tabellen aktivitet
        app_tables.aktivitet.add_row(
            deltager=user,
            dato=dato,
            aktivitet=aktivitet,
            poeng=poeng
        )
        return "Aktivitet lagret"


@anvil.server.callable
def hent_konkurranse():
    print('hent_konkurranse')
    # Hent alle poster med record lik 1
    konkurranse_records = app_tables.konkurranse.search(record=1)
    # Returner den første posten dersom den finnes, ellers None
    return konkurranse_records[0] if konkurranse_records else None

@anvil.server.callable
def lagre_trekning(uke_mandag):
    print('lagre_trekning')
    # Hent den påloggede brukeren
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")
    
    # Sjekk om en record med samme uke og bruker allerede finnes
    eksisterende = list(app_tables.trekning.search(uke_mandag=uke_mandag, deltager=user))
    if eksisterende:
        pass
    else:
        # Legg til ny record i tabellen 'trekning'
        app_tables.trekning.add_row(uke_mandag=uke_mandag, deltager=user)
    return ()

@anvil.server.callable
def slett_trekning(uke_mandag):
    print('slett_trekning')
    # Hent den påloggede brukeren
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")
    
    # Sjekk om en record med samme uke og bruker allerede finnes
    eksisterende = list(app_tables.trekning.search(uke_mandag=uke_mandag, deltager=user))
    # Dersom record finnes, slett den(e)
    for row in eksisterende:
        row.delete()
    return ()

@anvil.server.callable
def oppdater_brukernavn(nytt_navn):
    print('oppdater_brukernavn')
    # Hent den påloggede brukeren
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")
    
    # Søk etter en eksisterende record i UserInfo for denne brukeren
    record = app_tables.userinfo.get(user=user)
    
    if record:
        # Oppdater feltet 'navn' i den eksisterende recorden
        record['navn'] = nytt_navn
    else:
        # Opprett en ny record i tabellen UserInfo for denne brukeren
        app_tables.userinfo.add_row(user=user, navn=nytt_navn)
    
    return "Navn oppdatert"


@anvil.server.callable
def hent_brukernavn():
    print('hent_brukernavn')
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")
    
    record = app_tables.userinfo.get(user=user)
    
    if record is None:
        # print("❌ Fant ingen userinfo-rad for brukeren.")
        return {"navn": "", "team": ""}
    
    # Konverter record til en dictionary for å unngå LiveObject-problemer
    record_dict = dict(record)
    # print(f"✅ Fant userinfo-rad: {record_dict}")  # Debugging

    # Hent 'navn' eksplisitt
    navn = record_dict.get('navn', "")  # Bruker .get() for sikkerhet
    # print(f"📝 Navn hentet fra userinfo: {navn}")

    # Hent 'team' eksplisitt
    team_navn = ""
    if 'team' in record_dict and record_dict['team']:  # Sjekker at team ikke er None
        team_record = dict(record_dict['team'])  # Konverterer også team-raden til dict
        # print(f"🔍 Fant team-rad: {team_record}")  # Debugging
        team_navn = team_record.get('team', "")  # Henter team-navn

    # print(f"🏆 Endelig resultat: Navn = {navn}, Team = {team_navn}")

    return {"navn": navn, "team": team_navn}


      





import anvil.server

@anvil.server.callable
def hent_poengsummer():
    print('hent_poengsummer')
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
        navn = userinfo_rad['navn'] if userinfo_rad else None  # Hent navn hvis tilgjengelig
        email = deltager['email']  # Hent e-post direkte fra brukeren
        
        # Hent team hvis brukeren er knyttet til et
        team = userinfo_rad['team']['team'] if userinfo_rad and userinfo_rad['team'] else "Ingen team"

        # Fall tilbake til e-post hvis navn ikke finnes for deltager-feltet
        resultat.append({
            "deltager": navn if navn else email,
            "navn": navn,
            "email": email,
            "poeng": poeng,
            "team": team
        })

    # Sorter etter poeng, høyest først
    resultat.sort(key=lambda x: x["poeng"], reverse=True)

    return resultat


@anvil.server.callable
def hent_ukens_premietrekning(mandag):
    print('hent_ukens_premietrekning')
    import datetime

    # Sørg for at mandag er en date-type (dersom det blir sendt som en datetime)
    if isinstance(mandag, datetime.datetime):
        mandag = mandag.date()

    søndag = mandag + datetime.timedelta(days=6)  # Beregn søndag i samme uke
    
    # Dictionary for å holde styr på dager med poeng for hver deltaker
    deltager_dager = {}

    for rad in app_tables.aktivitet.search():
        deltager = rad['deltager']
        dato = rad['dato']  # Antar at 'dato' er en kolonne i 'aktivitet'

        # Sjekk om datoen er innenfor den uken vi skal hente
        if mandag <= dato <= søndag:
            if deltager:
                if deltager not in deltager_dager:
                    deltager_dager[deltager] = set()
                deltager_dager[deltager].add(dato)  # Legg til unike datoer

    # Filtrer ut deltakere med minst 5 ulike dager
    kvalifiserte = [deltager for deltager, dager in deltager_dager.items() if len(dager) >= 5]

    # Hent navn eller e-post for hver kvalifiserte deltaker
    resultat = []
    for deltager in kvalifiserte:
        userinfo_rad = app_tables.userinfo.get(user=deltager)
        navn = userinfo_rad['navn'] if userinfo_rad else None

        resultat.append(navn if navn else deltager['email'])

    return resultat



# @anvil.server.callable
# def hent_team_poengsummer():
#     print('hent_team_poengsummer')
#     # Dictionary for å holde styr på poeng per team
#     team_poeng = {}

#     # Hent alle brukere med tilhørende team
#     for userinfo in app_tables.userinfo.search():
#         team = userinfo['team']  # Henter team-raden
#         bruker = userinfo['user']  # Henter bruker-raden

#         if team and bruker:  # Sjekk at begge eksisterer
#             team_navn = team['team']  # Hent team-navn fra team-tabellen

#             # Initialiser teamet i dictionary hvis det ikke finnes
#             if team_navn not in team_poeng:
#                 team_poeng[team_navn] = 0

#             # Hent brukerens totale poengsum fra aktivitet-tabellen
#             bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
#             team_poeng[team_navn] += bruker_poeng  # Legg til poengene for teamet

#     # Konverter dictionary til en sortert liste (høyest poengsum først)
#     resultat = [{"team": team, "poengsum": poeng} for team, poeng in team_poeng.items()]
#     resultat.sort(key=lambda x: x["poengsum"], reverse=True)

#     print(f"🏆 Totale poengsummer per team: {resultat}")  # Debugging

#     return resultat

import anvil.server

@anvil.server.callable
def hent_team_poengsummer():
    print('hent_team_poengsummer')
    # Dictionary for å holde styr på poeng per team
    team_poeng = {}

    # Hent alle team fra team-tabellen for å sikre at alle vises
    for team in app_tables.team.search():
        team_navn = team['team']  # Hent team-navn
        team_poeng[team_navn] = 0  # Initialiser med 0 poeng

    # Hent alle brukere med tilhørende team
    for userinfo in app_tables.userinfo.search():
        team = userinfo['team']  # Henter team-raden
        bruker = userinfo['user']  # Henter bruker-raden

        if team and bruker:  # Sjekk at begge eksisterer
            team_navn = team['team']  # Hent team-navn fra team-tabellen
            
            # Hent brukerens totale poengsum fra aktivitet-tabellen
            bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
            team_poeng[team_navn] += bruker_poeng  # Legg til poengene for teamet

    # Konverter dictionary til en sortert liste (høyest poengsum først)
    resultat = [{"team": team, "poengsum": poeng} for team, poeng in team_poeng.items()]
    resultat.sort(key=lambda x: x["poengsum"], reverse=True)

    print(f"🏆 Totale poengsummer per team: {resultat}")  # Debugging

    return resultat



@anvil.server.callable
def create_user(email, name, password, team_name=None):
    print(f"Oppretter bruker: {email}")

    # Sjekk om brukeren allerede finnes
    existing_users = app_tables.users.search(email=email)
    if len(existing_users) > 0:
        print(f"Bruker {email} finnes allerede.")
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

@anvil.server.callable
def hent_teammedlemmer(team_navn):
    print(f"Henter medlemmer og poeng for team: {team_navn}")
    
    # Finn team-raden basert på navn
    team_record = app_tables.team.get(team=team_navn)

    if not team_record:
        print(f"❌ Fant ikke team med navn: {team_navn}")
        return []

    # Hent alle brukere i userinfo-tabellen som er tilknyttet dette teamet
    medlemmer = app_tables.userinfo.search(team=team_record)

    # Lag en liste med navn og total poengsum basert på aktivitetene deres
    team_liste = []
    for member in medlemmer:
        bruker = member['user']  # Hent bruker-raden (fra users-tabellen)
        if not bruker:
            continue  # Hopp over hvis user er None

        navn = member['navn']  # Hent navn fra userinfo-tabellen

        # Finn og summer poeng fra aktivitet-tabellen hvor brukeren er deltager
        poengsum = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))

        # Legg til i listen
        team_liste.append({"navn": navn, "poeng": poengsum})

    print(f"🏆 Teammedlemmer i {team_navn}: {team_liste}")
    return team_liste

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
        print(f"Team {team_navn} finnes ikke.")
        return "Teamet finnes ikke!"
    
    # Sjekk om det finnes brukere i dette teamet
    medlemmer = app_tables.userinfo.search(team=team)
    if len(medlemmer) > 0:
        print(f"Kan ikke slette {team_navn}, det har medlemmer.")
        return "Kan ikke slette teamet, det har medlemmer!"
    
    # Slett teamet
    team.delete()
    print(f"Team {team_navn} er slettet.")
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
        print("Eksisterende konkurranse oppdatert.")
    else:
        # Opprett ny rekord
        app_tables.konkurranse.add_row(
            record=1,
            konkurransenavn=konkurransenavn,
            fradato=fradato,
            tildato=tildato
        )
        print("Ny konkurranse opprettet.")
    
    return "Konkurranse lagret!"

@anvil.server.callable
def delete_user_by_email(email):
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
