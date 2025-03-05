# welcome.py
#
# Copyright 2024 mirkobrombin
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

import threading
import os
import pwd

_ = __builtins__["_"]

from gi.repository import Gtk, GLib, Adw

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/welcome-user.ui")
class VanillaWelcomeUser(Adw.Bin):
    __gtype_name__ = "VanillaWelcomeUser"

    btn_next = Gtk.Template.Child()
    btn_access = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        self.btn_next.connect("clicked", self.__on_btn_next_clicked)
        self.btn_access.connect("clicked", self.__on_btn_access_clicked)

        username = os.getlogin()
        full_name = pwd.getpwnam(username).pw_gecos.split(",")[0]
        
        message = _("Hello {}!").format(full_name)

        self.status_page.set_title(message)

    def set_page_active(self):
        self.__window.set_ready(True)
        self.btn_next.grab_focus()

    def set_page_inactive(self):
        return

    def finish(self):
        return True

    def __on_btn_next_clicked(self, widget):
        self.__window.finish_step()

    def __on_btn_access_clicked(self, widget):
        thread = threading.Thread(target=backend.open_accessibility_settings)
        thread.start()
