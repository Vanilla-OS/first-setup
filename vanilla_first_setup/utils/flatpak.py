import os
import subprocess


class Flatpak:
    env = os.environ.copy()

    @staticmethod
    def install(packages: list):
        proc = subprocess.Popen(
            ['flatpak', 'install', '--user'] + packages,
            env=Flatpak.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.communicate(input=b'y\n')

    @staticmethod
    def remove(packages: list):
        proc = subprocess.Popen(
            ['flatpak', 'remove', '--user'] + packages,
            env=Flatpak.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.communicate(input=b'y\n')

    @staticmethod
    def add_repo(repo: str):
        proc = subprocess.Popen(
            ['flatpak', 'remote-add', 'test', '--user', '--if-not-exists', repo],
            env=Flatpak.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.communicate(input=b'y\n')

        
