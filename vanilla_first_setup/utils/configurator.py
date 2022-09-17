import os
import time
import logging
import subprocess

from gi.repository import Gio

from vanilla_first_setup.utils import checks
from vanilla_first_setup.utils.apt import Apt
from vanilla_first_setup.utils.flatpak import Flatpak
from vanilla_first_setup.utils.snap import Snap


logger = logging.getLogger("FirstSetup::Configurator")


class Configurator:

    def __init__(self, config: 'Config', fake: bool = False):
        self.config = config
        self.fake = fake

    def apply(self):
        logging.info(f"Applying config: {self.config.get_str()}")
        self.__enable_snap() if self.config.snap else self.__disable_snap()
        self.__enable_flatpak() if self.config.flatpak else self.__disable_flatpak()
        self.__enable_appimage() if self.config.appimage else self.__disable_appimage()
        self.__enable_apport() if self.config.apport else self.__disable_apport()
        if self.config.apx:
            self.__enable_apx()
        if self.config.nvidia:
            self.__enable_nvidia()

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
    
    def __enable_appimage(self):
        if self.fake:
            return self.__fake("Fake: AppImage enabled")

        Apt.install(['fuse2'])
        Apt.update()
    
    def __disable_appimage(self):
        if self.fake:
            return self.__fake("Fake: AppImage disabled")

        # Apt.purge(['libfuse2']) # NOTE: we should not remove libfuse2, it may be needed by other packages at this point

    def __enable_apport(self):
        if self.fake:
            return self.__fake("Fake: Apport enabled")

        if not checks.is_apport_installed():
            Apt.install(['apport'])
            Apt.update()
            subprocess.run(['sudo', 'systemctl', 'start', 'apport.service'])

    def __disable_apport(self):
        if self.fake:
            return self.__fake("Fake: Apport disabled")

        if checks.is_apport_installed():
            subprocess.run(['sudo', 'systemctl', 'stop', 'apport.service'])
            Apt.purge(['apport'])
    
    def __enable_apx(self):
        if self.fake:
            return self.__fake("Fake: apx enabled")

        Apt.install(['curl', 'podman', 'apx'])
        Apt.update()

        proc = subprocess.run(['curl', '-s', 'https://raw.githubusercontent.com/89luca89/distrobox/main/install'], stdout=subprocess.PIPE)
        proc = subprocess.run(['sudo', 'sh'], input=proc.stdout, stdout=subprocess.PIPE)

    def __enable_nvidia(self):
        if self.fake:
            return self.__fake("Fake: Nvidia enabled")

        subprocess.run(['sudo', 'ubuntu-drivers', 'install', '--recommended'])

    def __disable_on_startup(self):
        if self.fake:
            return self.__fake("Fake: Disable on startup")

        autostart_file = os.path.expanduser("~/.config/autostart/io.github.vanilla-os.FirstSetup.desktop")
        if os.path.exists(autostart_file):
            os.remove(autostart_file)

    @staticmethod
    def reboot():
        subprocess.run(['gnome-session-quit', '--reboot'])
