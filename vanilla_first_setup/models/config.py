import logging


logger = logging.getLogger("FirstSetup::Config")


class Config:

    def __init__(
        self, 
        snap: bool, 
        flatpak: bool, 
        appimage: bool, 
        apport: bool, 
        distrobox: bool,
        nvidia: bool,
    ):
        self.snap = snap
        self.flatpak = flatpak
        self.appimage = appimage
        self.apport = apport
        self.distrobox = distrobox
        self.nvidia = nvidia

    def get_str(self) -> str:
        keys = [
            "snap", "flatpak", "appimage", "apport", "distrobox", "nvidia"
        ]
        vals = [
            self.snap, self.flatpak, self.appimage, self.apport, self.distrobox, self.nvidia
        ]
        return "|".join([f"{key}::{val}" for key, val in zip(keys, vals)])
    
    def set_val(self, key: str, val: bool):
        if key == "snap":
            self.snap = val
        elif key == "flatpak":
            self.flatpak = val
        elif key == "appimage":
            self.appimage = val
        elif key == "apport":
            self.apport = val
        elif key == "distrobox":
            self.distrobox = val
        elif key == "nvidia":
            self.nvidia = val
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
        appimage = items[2].split('::')[1]
        apport = items[3].split('::')[1]
        distrobox = items[4].split('::')[1]
        nvidia = items[5].split('::')[1]

        return cls(
            snap=get_bool(snap),
            flatpak=get_bool(flatpak),
            appimage=get_bool(appimage),
            apport=get_bool(apport),
            distrobox=get_bool(distrobox),
            nvidia=get_bool(nvidia),
        )
