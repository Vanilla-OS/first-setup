# user.py
#
# Copyright 2023 mirkobrombin
# Copyright 2023 muqtadir
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
import subprocess
from gi.repository import Gtk, Adw
_ = __builtins__["_"]

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/user.ui")
class VanillaUser(Adw.Bin):
    __gtype_name__ = "VanillaUser"

    fullname_entry = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    username_error = Gtk.Template.Child()

    username = ""
    __user_changed_username = False

    fullname = ""


    __automatic_username = ""

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        self.fullname_entry.connect("changed", self.__on_fullname_entry_changed)
        self.username_entry.connect("changed", self.__on_username_entry_changed)
        self.fullname_entry.connect("entry-activated", self.__on_activate)
        self.username_entry.connect("entry-activated", self.__on_activate)

        self.existing_users = subprocess.Popen("getent passwd | cut -d: -f1", shell=True,
                                          stdout=subprocess.PIPE).stdout.read().decode().splitlines()

    def set_page_active(self):
        self.fullname_entry.grab_focus()
        self.__verify_continue()

    def set_page_inactive(self):
        return

    def finish(self):
        backend.add_user_deferred(self.username, self.fullname)
        return True

    def __on_activate(self, widget):
        self.__window.finish_step()

    def __on_fullname_entry_changed(self, *args):
        fullname = self.fullname_entry.get_text()

        self.fullname = fullname
        self.__verify_continue()

        self.__generate_username_from_fullname()

    def __on_username_entry_changed(self, *args):
        entry_text = self.username_entry.get_text()
        if entry_text != "" and entry_text != self.__automatic_username:
            self.__user_changed_username = True

        err = self.__verify_username()

        if err != "":
            self.username = ""
            self.username_entry.add_css_class("error")
            self.username_error.set_label(err)
            self.username_error.set_opacity(1)
            self.__verify_continue()
            return

        self.username = entry_text
        self.username_entry.remove_css_class("error")
        self.username_error.set_opacity(0)
        self.__verify_continue()

    def __generate_username_from_fullname(self):
        if self.__user_changed_username:
            return

        if self.fullname == "":
            return

        username_stripped = self.fullname.strip()
        username_no_whitespace = "-".join(username_stripped.split())
        username_lowercase = username_no_whitespace.lower()

        self.__automatic_username = username_lowercase
        self.username_entry.set_text(username_lowercase)

    def __verify_continue(self):
        ready = self.username != "" and self.fullname != ""
        self.__window.set_ready(ready)

    def __verify_username(self) -> str:
        input = self.username_entry.get_text()

        if not input:
            return _("Username cannot be empty.")

        if len(input) > 32:
            return _("Username cannot be longer than 32 characters.")

        if re.search(r"[^a-z0-9_-]", input):
            return _("Username cannot contain special characters or uppercase letters.")

        if input in self.existing_users:
            _status = False
            return _("This username is already in use.")
        
        return ""
