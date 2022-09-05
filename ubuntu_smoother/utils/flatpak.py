import subprocess


class Flatpak:

    @staticmethod
    def install(self, packages: list):
        subprocess.run(
            ['flatpak', 'install', '--user'] + packages,
            check=True
        )

    @staticmethod
    def remove(self, packages: list):
        subprocess.run(
            ['flatpak', 'remove', '--user'] + packages,
            check=True
        )

    @staticmethod
    def add_repo(self, repo: str):
        subprocess.run(
            ['flatpak', 'remote-add', '--user', '--if-not-exists', repo],
            check=True
        )
