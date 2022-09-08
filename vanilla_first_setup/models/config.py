import logging


logger = logging.getLogger("FirstSetup::Config")


class Config:

    def __init__(self, snap: bool, flatpak: bool, apport: bool, distrobox: bool):
        self.snap = snap
        self.flatpak = flatpak
        self.apport = apport
        self.distrobox = distrobox

    def get_str(self) -> str:
        return "snap::{0}|flatpak::{1}|apport::{2}|distrobox::{3}".format(
            self.snap, self.flatpak, self.apport, self.distrobox
        )
    
    def set_val(self, key: str, val: bool):
        if key == "snap":
            self.snap = val
        elif key == "flatpak":
            self.flatpak = val
        elif key == "apport":
            self.apport = val
        elif key == "distrobox":
            self.distrobox = val
        else:
            return
            
        logger.info(f"Setting {key} to {val}")

    @classmethod
    def from_str(cls, config_str: str) -> 'Config':
        def get_bool(value: str):
            return "True" in value

        items = config_str.split('|')

        snap = items[0].split('::')[1]
        flatpak = items[1].split('::')[1]
        apport = items[2].split('::')[1]
        distrobox = items[3].split('::')[1]

        return cls(
            snap=get_bool(snap),
            flatpak=get_bool(flatpak),
            apport=get_bool(apport),
            distrobox=get_bool(distrobox)
        )
