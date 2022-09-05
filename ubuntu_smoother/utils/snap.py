import subprocess


class Snap:

    @staticmethod
    def install(self, packages: list):
        subprocess.run(
            ['snap', 'install'] + packages,
            check=True
        )

    @staticmethod
    def remove(self, packages: list):
        subprocess.run(
            ['snap', 'remove'] + packages,
            check=True
        )
