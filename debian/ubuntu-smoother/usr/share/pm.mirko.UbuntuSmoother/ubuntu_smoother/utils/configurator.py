import os
import time
import logging

from sugar_cubes.utils import checks
from sugar_cubes.utils.apt import Apt
from sugar_cubes.utils.flatpak import Flatpak
from sugar_cubes.utils.snap import Snap


logger = logging.getLogger("SugarCubes::Configurator")


class Configurator:

    def __init__(self, config: 'Config', fake: bool = False):
        self.config = config
        self.fake = fake

    def apply(self):
        self.__enable_snap() if self.config.snap else self.__disable_snap()
        self.__enable_flatpak() if self.config.flatpak else self.__disable_flatpak()
        self.__enable_apport() if self.config.apport else self.__disable_apport()

    def __fake(self, msg: str):
        time.sleep(1)
        logger.info(f"Fake: {msg}")

    def __enable_snap(self):
        if self.fake:
            return self.__fake("Fake: Snap enabled")

        if not checks.is_snap_installed():
            Apt.install(['snapd', 'gnome-software-plugin-snap'])
            Apt.update()

        if not self.config.flatpak:
            Snap.install(['snap-store'])

    def __disable_snap(self):
        if self.fake:
            return self.__fake("Fake: Snap disabled")

        if checks.is_snap_installed():
            Apt.purge(['snapd'])

    def __enable_flatpak(self):
        if self.fake:
            return self.__fake("Fake: Flatpak enabled")

        if not checks.is_flatpak_installed():
            Apt.install(['flatpak'])
            Apt.update()
            Flatpak.add_repo("https://flathub.org/repo/flathub.flatpakrepo")

    def __disable_flatpak(self):
        if self.fake:
            return self.__fake("Fake: Flatpak disabled")

        if checks.is_flatpak_installed():
            Apt.purge(['flatpak'])

    def __enable_apport(self):
        if self.fake:
            return self.__fake("Fake: Apport enabled")

        if not checks.is_apport_installed():
            Apt.install(['apport'])
            Apt.update()

    def __disable_apport(self):
        if self.fake:
            return self.__fake("Fake: Apport disabled")

        if checks.is_apport_installed():
            Apt.purge(['apport'])

    def __disable_on_startup(self):
        if self.fake:
            return self.__fake("Fake: Disable on startup")

        autostart_file = os.path.expanduser("~/.config/autostart/sugar-cubes.desktop")
        if os.path.exists(autostart_file):
            os.remove(autostart_file)

    def __enable_on_startup(self):
        if self.fake:
            return self.__fake("Fake: Enable on startup")

        autostart_file = os.path.expanduser("~/.config/autostart/sugar-cubes.desktop")
        if not os.path.exists(autostart_file):
            with open(autostart_file, "w") as f:
                f.write("[Desktop Entry]")
                f.write("Type=Application")
                f.write("Name=Sugar Cubes")
                f.write("Exec=sugar-cubes")
                f.write("Terminal=false")
                f.write("X-GNOME-Autostart-enabled=true")
                