from ._anvil_designer import EditDayTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EditDay(EditDayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dato =  "date": datetime.date.today()}
    self.date_picker.date = self.day["date"]
    self.activity_box.text = self.day["activity"]

    # Any code you write here will run before the form opens.

  def save_button_click(self, **event_args):
    for rb in self.get_components():
        if isinstance(rb, RadioButton) and rb.group_name == "poeng" and rb.selected:
            chosen_value = rb.text
            break
    alert(f"Du valgte: {chosen_value}")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    for rb in self.radio_panel.get_components():
      if isinstance(rb, RadioButton) and rb.group_name == "poeng" and rb.selected:
          chosen_value = rb.text
          break
    alert(f"Du valgte: {chosen_value}")
