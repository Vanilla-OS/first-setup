import subprocess
import shutil


def is_snap_installed():
    return shutil.which('snap') is not None


def is_flatpak_installed():
    return shutil.which('flatpak') is not None


def is_apport_installed():
    return shutil.which('apport') is not None


def has_nvidia_gpu():
    return subprocess.run(['lspci'], stdout=subprocess.PIPE).stdout.decode('utf-8').find('VGA compatible controller: NVIDIA Corporation') != -1
