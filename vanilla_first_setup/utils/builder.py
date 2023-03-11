# builder.py
#
# Copyright 2022 mirkobrombin
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
import subprocess

from vanilla_first_setup.utils.recipe import RecipeLoader

from vanilla_first_setup.defaults.conn_check import VanillaDefaultConnCheck
from vanilla_first_setup.defaults.welcome import VanillaDefaultWelcome
from vanilla_first_setup.defaults.theme import VanillaDefaultTheme
from vanilla_first_setup.defaults.user import VanillaDefaultUser
from vanilla_first_setup.defaults.hostname import VanillaDefaultHostname

from vanilla_first_setup.layouts.preferences import VanillaLayoutPreferences
from vanilla_first_setup.layouts.yes_no import VanillaLayoutYesNo
from vanilla_first_setup.defaults.applications import VanillaLayoutApplications


logger = logging.getLogger("FirstSetup::Builder")


templates = {
    "conn-check": VanillaDefaultConnCheck,
    "welcome": VanillaDefaultWelcome,
    "theme": VanillaDefaultTheme,
    "user": VanillaDefaultUser,
    "hostname": VanillaDefaultHostname,
    "preferences": VanillaLayoutPreferences,
    "yes-no": VanillaLayoutYesNo,
    "applications": VanillaLayoutApplications
}


class Builder:

    def __init__(self, window, new_user: bool = False):
        self.__window = window
        self.__new_user = new_user
        self.__recipe = RecipeLoader()
        self.__register_widgets = []
        self.__register_finals = []
        self.__load()

    def __load(self):
        # here we create a temporary file to store the output of the commands
        # the log path is defined in the recipe
        if "log_file" not in self.__recipe.raw:
            logger.critical("Missing 'log_file' in the recipe.")
            sys.exit(1)

        log_path = self.__recipe.raw["log_file"]

        if not os.path.exists(log_path):
            try:
                open(log_path, 'a').close()
            except OSError:
                logger.warning("failed to create log file: %s" % log_path)
                logging.warning("No log will be stored.")

        for key, step in self.__recipe.raw["steps"].items():
            _status = True
            _protected = False

            if step.get("display-conditions"):
                _condition_met = False
                for command in step["display-conditions"]:
                    try:
                        logger.info("Performing display-condition: %s" % command)
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                        if output.decode("utf-8") == "" or output.decode("utf-8") == "1":
                            logger.info("Step %s skipped due to display-conditions" % key)
                            break
                    except subprocess.CalledProcessError as e:
                        logger.info("Step %s skipped due to display-conditions" % key)
                        break
                else:
                    _condition_met = True

                if not _condition_met:
                    continue
                    
                if step.get("new-user-only") and not self.__new_user:
                    continue
            
            _status = not step.get("is-advanced", False)

            if step.get("protected"):
                _protected = True

            if step["template"] in templates:
                _widget = templates[step["template"]](self.__window, self.distro_info, key, step)
                self.__register_widgets.append((_widget, _status, _protected))

    def get_temp_finals(self, step_id: str):
        for widget, _, _ in self.__register_widgets:
            if widget.step_id == step_id:
                return widget.get_finals()

        return None

    def get_finals(self):
        self.__register_finals = []

        for widget, _, _ in self.__register_widgets:
            self.__register_finals.append(widget.get_finals())

        return self.__register_finals

    @property
    def widgets(self):
        return self.__register_widgets

    @property
    def recipe(self):
        return self.__recipe.raw

    @property
    def distro_info(self):
        return {
            "name": self.__recipe.raw["distro_name"],
            "logo": self.__recipe.raw["distro_logo"]
        }
