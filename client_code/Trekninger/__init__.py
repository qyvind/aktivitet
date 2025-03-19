class Trekninger(TrekningerTemplate):
  def __init__(self, aktiv_mandag=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Hvis ikke mandag er sendt inn, bruk dagens uke
    if aktiv_mandag is None:
      idag = datetime.date.today()
      aktiv_mandag = idag - datetime.timedelta(days=idag.weekday())  # Finn mandagen i uken

    # Kall serverfunksjonen med aktiv mandag
    liste = anvil.server.call('hent_ukens_premietrekning', aktiv_mandag)
    print(liste)

  def lukk_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Loggbok")