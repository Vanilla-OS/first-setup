import subprocess


class Snap:

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['snap', 'install'] + packages,
            check=True
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['snap', 'remove'] + packages,
            check=True
        )
