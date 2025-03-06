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
  print('server called')
  if aktivitet.get('dato') and aktivitet.get('aktivitet') and aktivitet.get('poeng') :
     app_tables.aktivitet.add_row(**aktivitet)
