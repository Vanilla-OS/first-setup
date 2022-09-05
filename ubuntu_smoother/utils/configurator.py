import logging

from ubuntu_smoother.utils import checks
from ubuntu_smoother.utils.apt import Apt
from ubuntu_smoother.utils.flatpak import Flatpak
from ubuntu_smoother.utils.snap import Snap


logger = logging.getLogger("UbuntuSmoother::Configurator")

class Configurator:

    def __init__(self, config: 'Config', fake: bool = False):
        self.config = config
        self.fake = fake

    def apply(self):
        self.__enable_snap() if self.config.snap else self.__disable_snap()
        self.__enable_flatpak() if self.config.flatpak else self.__disable_flatpak()
        self.__enable_apport() if self.config.apport else self.__disable_apport()
    
    def __enable_snap(self):
        if self.fake:
            logger.info("Fake: Snap enabled")
            return

        pkgs = []
        if not checks.is_snap_installed():
            pkgs += ['snapd', 'gnome-software-plugin-snap']
        Apt.install(pkgs)
        Apt.update()

        if not self.config.flatpak:
            Snap.install(['snap-store'])
            
    def __disable_snap(self):
        if self.fake:
            logger.info("Fake: Snap disabled")
            return

        if checks.is_snap_installed():
            Apt.purge(['snapd'])
            
    def __enable_flatpak(self):
        if self.fake:
            logger.info("Fake: Flatpak enabled")
            return

        if not checks.is_flatpak_installed():
            Apt.install(['flatpak'])
            Flatpak.add_repo("https://flathub.org/repo/flathub.flatpakrepo")
        Apt.update()

    def __disable_flatpak(self):
        if self.fake:
            logger.info("Fake: Flatpak disabled")
            return

        if checks.is_flatpak_installed():
            Apt.purge(['flatpak'])

    def __enable_apport(self):
        if self.fake:
            logger.info("Fake: Apport enabled")
            return

        if not checks.is_apport_installed():
            Apt.install(['apport'])
        Apt.update()

    def __disable_apport(self):
        if self.fake:
            logger.info("Fake: Apport disabled")
            return

        if checks.is_apport_installed():
            Apt.purge(['apport'])
