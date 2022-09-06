import subprocess


class Flatpak:

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['flatpak', 'install', '--user'] + packages,
            check=True
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['flatpak', 'remove', '--user'] + packages,
            check=True
        )

    @staticmethod
    def add_repo(repo: str):
        subprocess.run(
            ['flatpak', 'remote-add', '--user', '--if-not-exists', repo],
            check=True
        )
