import logging
import subprocess


logger = logging.getLogger("FirstSetup::Processor")


class Processor:

    def __init__(self, config: 'Config'):
        self.__config = config

    def run(self):
        logger.info(f"Spawning processor with config: {self.__config.get_str()}")

        proc = subprocess.run(
            ["pkexec", "vanilla-first-setup-processor", self.__config.get_str()], 
            check=True
        )
        
        if proc.returncode != 0:
            return False, "Error executing the Vanilla OS First Setup Processor"

        return True