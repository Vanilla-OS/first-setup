import os
import subprocess


class Flatpak:
    env = os.environ.copy()

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['flatpak', 'install', '--user'] + packages,
            env=Flatpak.env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['flatpak', 'remove', '--user'] + packages,
            env=Flatpak.env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    @staticmethod
    def add_repo(repo: str):
        subprocess.run(
            ['flatpak', 'remote-add', '--user', '--if-not-exists', repo],
            env=Flatpak.env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
