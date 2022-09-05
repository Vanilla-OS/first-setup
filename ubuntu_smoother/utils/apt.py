import subprocess


class Apt:

    @staticmethod
    def install(self, packages: list):
        subprocess.run(
            ['sudo', 'apt', 'install'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def remove(self, packages: list):
        subprocess.run(
            ['sudo', 'apt', 'remove'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def purge(self, packages: list):
        subprocess.run(
            ['sudo', 'apt', 'purge'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def update(self):
        subprocess.run(
            ['sudo', 'apt', 'update'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def upgrade(self):
        subprocess.run(
            ['sudo', 'apt', 'upgrade'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )
