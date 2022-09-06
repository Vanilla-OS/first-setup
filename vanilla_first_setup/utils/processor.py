import subprocess


class Processor:

    def __init__(self, config: 'Config'):
        self.__config = config

    def run(self):
        proc = subprocess.run(
            ["pkexec", "vanilla-first-setup-processor", self.__config.get_str()], 
            check=True
        )
        
        if proc.returncode != 0:
            return False, "Error executing the Vanilla OS First Setup Processor"

        return True