import subprocess


class Apt:

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'install'] + packages + ['-y'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'remove'] + packages + ['-y'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )

    @staticmethod
    def purge(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'purge'] + packages + ['-y'],
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
            ['sudo', 'apt', 'upgrade', '-y'],
            env={'DEBIAN_FRONTEND': 'noninteractive'},
            check=True
        )
