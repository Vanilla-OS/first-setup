from ubuntu_smoother.utils import checks
from ubuntu_smoother.utils.apt import Apt
from ubuntu_smoother.utils.flatpak import Flatpak
from ubuntu_smoother.utils.snap import Snap


class Configurator:

    def __init__(self, config: 'Config'):
        self.config = config

    def apply(self):
        self.__enable_snap() if self.config.snap else self.__disable_snap()
        self.__enable_flatpak() if self.config.flatpak else self.__disable_flatpak()
        self.__enable_apport() if self.config.apport else self.__disable_apport()
    
    def __enable_snap(self):
        pkgs = []
        if not checks.is_snap_installed():
            pkgs += ['snapd', 'gnome-software-plugin-snap']
        Apt.install(pkgs)
        Apt.update()

        if not self.config.flatpak:
            Snap.install(['snap-store'])
            
    def __disable_snap(self):
        if checks.is_snap_installed():
            Apt.purge(['snapd'])
            
    def __enable_flatpak(self):
        if not checks.is_flatpak_installed():
            Apt.install(['flatpak'])
            Flatpak.add_repo("https://flathub.org/repo/flathub.flatpakrepo")
        Apt.update()

    def __disable_flatpak(self):
        if checks.is_flatpak_installed():
            Apt.purge(['flatpak'])
