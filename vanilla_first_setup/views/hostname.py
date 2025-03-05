# hostname.py
#
# Copyright 2023 mirkobrombin
#
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

import re
from gi.repository import Gtk, Adw

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/hostname.ui")
class VanillaHostname(Adw.Bin):
    __gtype_name__ = "VanillaHostname"

    hostname_entry = Gtk.Template.Child()
    hostname_error = Gtk.Template.Child()

    hostname = ""

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        # signals
        self.hostname_entry.connect("changed", self.__on_hostname_entry_changed)
        self.hostname_entry.connect("entry-activated", self.__on_activate)

    def set_page_active(self):
        self.hostname_entry.grab_focus()
        self.__verify_continue()

    def set_page_inactive(self):
        return

    def finish(self):
        return backend.set_hostname(self.hostname)

    def __on_activate(self, widget):
        self.__window.finish_step()

    def __on_hostname_entry_changed(self, *args):
        _hostname = self.hostname_entry.get_text()

        if self.__validate_hostname(_hostname):
            self.hostname = _hostname
            self.hostname_entry.remove_css_class("error")
            self.hostname_error.set_opacity(0.0)
            self.__verify_continue()
            return

        self.hostname_entry.add_css_class("error")
        self.hostname = ""
        self.hostname_error.set_opacity(1.0)
        self.__verify_continue()

    def __validate_hostname(self, hostname):
        if len(hostname) > 64:
            return False

        lower_ascii = re.compile(r"[a-z]+$")

        dot_parts = hostname.split(".")
        for dot_part in dot_parts:
            hyphen_parts = dot_part.split("-")
            for hyphen_part in hyphen_parts:
                if not lower_ascii.match(hyphen_part):
                    return False

        return True

    def __verify_continue(self):
        ready = self.hostname != ""
        self.__window.set_ready(ready)
