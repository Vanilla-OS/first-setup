import shutil


def is_snap_installed():
    return shutil.which('snap') is not None


def is_flatpak_installed():
    return shutil.which('flatpak') is not None


def is_apport_installed():
    return shutil.which('apport') is not None
