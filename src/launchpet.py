import subprocess
import sys
import pathlib
import logging
from PySide6.QtCore import Slot, QObject

class PetLauncher(QObject):
    # ... your existing setup ...

    @Slot()
    def launch_pet_room(self):
        """Launches the Tkinter application as an independent background process."""
        # 1. Locate the script safely relative to this current file
        base_path = pathlib.Path(__file__).parent.resolve()
        script_path = base_path / "PetLedger" / "main.py" # Change to your actual filename/path

        if not script_path.exists():
            logging.error(f"Cannot launch script: {script_path} does not exist.")
            return

        logging.info(f"Launching external Tkinter application: {script_path}")

        # 2. Use the current environment's python executable to guarantee dependencies match
        subprocess.Popen(
            [sys.executable, str(script_path)]
        )
