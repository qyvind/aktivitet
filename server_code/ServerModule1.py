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


@anvil.server.callable
def batch_create_users(user_list):
    print('batch_create_users')
    for user in user_list:
        email, password = user["email"], user["password"]

        # Sjekk om brukeren allerede finnes
        existing_users = app_tables.users.search(email=email)
        if len(existing_users) > 0:
            print(f"Bruker {email} finnes allerede, hopper over.")
            continue  # Hopp over eksisterende brukere

        # Opprett ny bruker med Anvils innebygde metode
        anvil.users.signup_with_email(email, password)

        print(f"Bruker {email} opprettet.")

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


      



@anvil.server.callable
def hent_poengsummer():
    print('hent_poengsummer')
    poeng_dict = {}

    for rad in app_tables.aktivitet.search():
        deltager = rad['deltager']  # Link til user-tabellen
        poeng = rad['poeng']

        if deltager:
            if deltager not in poeng_dict:
                poeng_dict[deltager] = 0
            poeng_dict[deltager] += poeng

    # Konverter til liste med navn hvis tilgjengelig, ellers e-post
    resultat = []
    for deltager, poeng in poeng_dict.items():
        userinfo_rad = app_tables.userinfo.get(user=deltager)  # Hent userinfo basert på user-link
        navn = userinfo_rad['navn'] if userinfo_rad else None  # Hent navn hvis tilgjengelig

        # Fall tilbake til e-post hvis navn ikke finnes
        resultat.append({
            "deltager": navn if navn else deltager['email'],
            "poeng": poeng
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

@anvil.server.callable
def hent_teammedlemmer(team_navn):
    print('hent_teammedlemmer')
    # Finn team-raden basert på navn
    team_record = app_tables.team.get(team=team_navn)

    if not team_record:
        # print(f"❌ Fant ikke team med navn: {team_navn}")
        return []

    # print(f"✅ Fant team: {dict(team_record)}")  # Debugging

    # Hent alle brukere i userinfo-tabellen som er tilknyttet dette teamet
    medlemmer = app_tables.userinfo.search(team=team_record)

    # Lag en liste med navnene på teammedlemmene
    team_liste = [member['navn'] for member in medlemmer if member['navn']]

    # print(f"🏆 Teammedlemmer i {team_navn}: {team_liste}")

    return team_liste

@anvil.server.callable
def hent_team_poengsummer():
    print('hent_team_poengsummer')
    # Dictionary for å holde styr på poeng per team
    team_poeng = {}

    # Hent alle brukere med tilhørende team
    for userinfo in app_tables.userinfo.search():
        team = userinfo['team']  # Henter team-raden
        bruker = userinfo['user']  # Henter bruker-raden

        if team and bruker:  # Sjekk at begge eksisterer
            team_navn = team['team']  # Hent team-navn fra team-tabellen

            # Initialiser teamet i dictionary hvis det ikke finnes
            if team_navn not in team_poeng:
                team_poeng[team_navn] = 0

            # Hent brukerens totale poengsum fra aktivitet-tabellen
            bruker_poeng = sum(rad['poeng'] for rad in app_tables.aktivitet.search(deltager=bruker))
            team_poeng[team_navn] += bruker_poeng  # Legg til poengene for teamet

    # Konverter dictionary til en sortert liste (høyest poengsum først)
    resultat = [{"team": team, "poengsum": poeng} for team, poeng in team_poeng.items()]
    resultat.sort(key=lambda x: x["poengsum"], reverse=True)

    print(f"🏆 Totale poengsummer per team: {resultat}")  # Debugging

    return resultat
