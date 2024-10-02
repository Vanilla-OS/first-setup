# welcome.py
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

import time
import sys
from gi.repository import Gtk, GLib, Adw
from gettext import translation
from vanilla_first_setup.utils.recipe import RecipeLoader

from vanilla_first_setup.utils.run_async import RunAsync
from vanilla_first_setup.core.languages import all_locale


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/default-welcome.ui")
class VanillaDefaultWelcome(Adw.Bin):
    __gtype_name__ = "VanillaDefaultWelcome"

    btn_advanced = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    status_page = Gtk.Template.Child()
    title_label = Gtk.Template.Child()
    welcome_message = Gtk.Template.Child()

    def validate_advanced(self):
        recipeLoader = RecipeLoader()
        for i in recipeLoader.raw["steps"].items():
            try:
                if i[1]["is-advanced"] == True:
                    return
            except:
                pass

        self.btn_advanced.set_sensitive(False)

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        self.validate_advanced()

        # animation start
        self.__start_welcome_animation()

        # signals
        self.btn_advanced.connect("clicked", self.__advanced)
        self.btn_next.connect("clicked", self.__next)

        # set distro logo
        self.status_page.set_icon_name(self.__distro_info["logo"])

    @property
    def step_id(self):
        return self.__key

    def __start_welcome_animation(self):
        def change_langs():
            while True:
                for locale in all_locale:
                    translator = translation('vanilla-first-setup', localedir=f"{sys.base_prefix}/share/locale", languages=[locale], fallback=True)
                    _ = translator.gettext
                    GLib.idle_add(self.title_label.set_text, _("Welcome!"))
                    GLib.idle_add(self.btn_next.set_label, _("Next"))
                    GLib.idle_add(self.btn_advanced.set_label, _("Advanced"))
                    GLib.idle_add(self.welcome_message.set_label, _("Make your choices, this wizard will take care of everything."))
                    time.sleep(2.0)

        RunAsync(change_langs, None)

    def __advanced(self, widget):
        self.__window.next(rebuild=True, mode=1)

    def __next(self, widget):
        self.__window.next(rebuild=True, mode=0)

    def get_finals(self):
        return {}
