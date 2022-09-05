import subprocess


class Apt:

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'install'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'remove'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def purge(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'purge'] + packages,
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def update():
        subprocess.run(
            ['sudo', 'apt', 'update'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def upgrade():
        subprocess.run(
            ['sudo', 'apt', 'upgrade'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )
