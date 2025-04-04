from ._anvil_designer import IkonPickerFormTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables




class IconPickerForm(IconPickerFormTemplate):

    def __init__(self, **properties):
        self.init_components(**properties)

        from anvil.tables import app_tables

        icons = app_tables.files.search()
        self.repeating_panel_1.items = [
            {"file": row["file"]} for row in icons
            if row["file"].content_type.startswith("image/")
        ]

    def image_click(self, **event_args):
        # Returner valgt ikon til alert-caller
        alert.dismiss(self.item["file"])

