# recipe.py
#
# Copyright 2023 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import logging
import json


logger = logging.getLogger("FirstSetup::RecipeLoader")


class RecipeLoader:
    recipe_path = "/usr/share/org.vanillaos.FirstSetup/recipe.json"

    def __init__(self):
        self.__recipe = {}
        self.__load()

    def __load(self):
        if "VANILLA_CUSTOM_RECIPE" in os.environ:
            self.recipe_path = os.environ["VANILLA_CUSTOM_RECIPE"]

        logger.info(f"Loading recipe from {self.recipe_path}")

        if os.path.exists(self.recipe_path):
            with open(self.recipe_path, "r") as f:
                self.__recipe = json.load(f)
                return

        if not self.__validate():
            logger.error("Invalid recipe file")
            sys.exit(1)

        logger.error(f"Recipe not found at {self.recipe_path}")
        sys.exit(1)

    def __validate(self):
        essential_keys = ["log_file", "distro_name", "distro_logo", "steps"]
        if not isinstance(self.__recipe, dict):
            logger.error("Recipe is not a dictionary")
            return False

        for key in essential_keys:
            if key not in self.__recipe:
                logger.error(f"Recipe is missing the '{key}' key")
                return False

        if not isinstance(self.__recipe["steps"], list):
            logger.error("Recipe steps is not a list")
            return False

        for step in self.__recipe["steps"]:
            if not isinstance(step, dict):
                logger.error(f"Step {step} is not a dictionary")
                return False

    @property
    def raw(self):
        return self.__recipe
