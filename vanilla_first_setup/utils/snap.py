import os
import subprocess


class Snap:
    env = os.environ.copy()

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['sudo', 'snap', 'install'] + packages,
            env=Snap.env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['sudo', 'snap', 'remove'] + packages,
            env=Snap.env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
