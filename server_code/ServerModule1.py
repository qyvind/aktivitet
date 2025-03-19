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
  
  if aktivitet.get('dato') and aktivitet.get('aktivitet') and aktivitet.get('poeng') :
    app_tables.aktivitet.add_row(**aktivitet)

@anvil.server.callable
def update_aktivitet(aktivitet, aktivitet_data):
  
  if aktivitet_data['dato'] and aktivitet_data['aktivitet'] and aktivitet_data['poeng']: 
    aktivitet.update(**aktivitet_data)

@anvil.server.callable
def delete_aktivitet(aktivitet):
  aktivitet.delete()


@anvil.server.callable
def batch_create_users(user_list):
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
    # Hent alle poster med record lik 1
    konkurranse_records = app_tables.konkurranse.search(record=1)
    # Returner den første posten dersom den finnes, ellers None
    return konkurranse_records[0] if konkurranse_records else None

@anvil.server.callable
def lagre_trekning(uke_mandag):
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
    user = anvil.users.get_user()
    if not user:
        raise Exception("Bruker ikke logget inn")
    
    record = app_tables.userinfo.get(user=user)
    if record is None:
        return ""  # Returnerer tom streng hvis ingen record finnes
    
    return record['navn']


      



@anvil.server.callable
def hent_poengsummer():
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
def hent_ukens_premietrekning():
    import datetime

    # Finn dagens dato
    idag = datetime.date.today()

    # Finn mandagen i inneværende uke
    mandag = idag - datetime.timedelta(days=idag.weekday())  # Mandag = weekday() == 0
    søndag = mandag + datetime.timedelta(days=6)

    # Dictionary for å holde styr på dager med poeng for hver deltaker
    deltager_dager = {}

    for rad in app_tables.aktivitet.search():
        deltager = rad['deltager']
        dato = rad['dato']  # Antar at 'dato' er en kolonne i 'aktivitet'

        # Sjekk om datoen er innenfor inneværende uke
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
