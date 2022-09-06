import subprocess


class Processor:

    def __init__(self, config: 'Config'):
        self.__config = config

    def run(self):
        proc = subprocess.run(
            ["pkexec", "sugar-cubes-processor", self.__config.get_str()], 
            check=True
        )
        
        if proc.returncode != 0:
            return False, "Error executing the Sugar Cubes Processor"

        return True