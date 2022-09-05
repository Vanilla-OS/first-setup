class Config:

    def __init__(self, snap: bool, flatpak: bool, apport: bool):
        self.snap = snap
        self.flatpak = flatpak
        self.apport = apport

    def get_str(self) -> str:
        return "snap::{0}|flatpak::{1}|apport::{2}".format(
            self.snap, self.flatpak, self.apport
        )
    
    @classmethod
    def from_str(cls, config_str: str) -> 'Config':
        items = config_str.split('|')
        
        snap = items[0].split('::')[1]
        flatpak = items[1].split('::')[1]
        apport = items[2].split('::')[1]

        return cls(
            snap=bool(snap),
            flatpak=bool(flatpak),
            apport=bool(apport)
        )
