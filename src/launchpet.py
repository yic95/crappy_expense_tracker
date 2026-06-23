import subprocess
import sys
import pathlib
import logging
from PySide6.QtCore import Slot, QObject
import appdirs
from datetime import date, timedelta

class PetLauncher(QObject):
    def __init__(self, parent=None, objname=str, *,expense_service):
        super().__init__(parent)
        self.service = expense_service

    def get_coin_amount(self) -> int:
        entries = self.service.read(date.today() - timedelta(60), date.today())
        entries_recent = [di for di in entries if di['date'] >= date.today() - timedelta(3)]
        avg_entries = sum([ent['expense'] for ent in entries]) / len(entries)
        avg_entries_recent = sum([ent['expense'] for ent in entries_recent]) / len(entries_recent)
        return max(100, (10 * avg_entries_recent - avg_entries))

    @Slot()
    def launch_pet_room(self):
        # 1. Locate the script safely relative to this current file
        base_path = pathlib.Path(__file__).parent.resolve()
        script_path = base_path / "PetLedger" / "main.py" # Change to your actual filename/path

        if not script_path.exists():
            logging.error(f"Cannot launch script: {script_path} does not exist.")
            return

        logging.info(f"Launching external Tkinter application: {script_path}")

        # 2. Use the current environment's python executable to guarantee dependencies match
        subprocess.Popen([sys.executable, str(script_path), str(self.get_coin_amount())])
