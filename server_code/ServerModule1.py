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

'''
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
'''