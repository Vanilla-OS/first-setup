import os
import subprocess


class Apt:

    env = os.environ.copy()
    env['DEBIAN_FRONTEND'] = 'noninteractive'

    @staticmethod
    def install(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'install'] + packages + ['-y'],
            env=Apt.env,
            check=True
        )

    @staticmethod
    def remove(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'remove'] + packages + ['-y'],
            env=Apt.env,
            check=True
        )

    @staticmethod
    def purge(packages: list):
        subprocess.run(
            ['sudo', 'apt', 'purge'] + packages + ['-y'],
            env=Apt.env,
            check=True
        )

    @staticmethod
    def update():
        subprocess.run(
            ['sudo', 'apt', 'update'],
            env=Apt.env,
            check=True
        )

    @staticmethod
    def upgrade():
        subprocess.run(
            ['sudo', 'apt', 'upgrade', '-y'],
            env=Apt.env,
            check=True
        )
