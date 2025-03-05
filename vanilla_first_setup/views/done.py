# done.py
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

import subprocess

_ = __builtins__["_"]
from gi.repository import Gtk, Adw

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/done.ui")
class VanillaDone(Adw.Bin):
    __gtype_name__ = "VanillaDone"

    status_page = Gtk.Template.Child()
    btn_tour = Gtk.Template.Child()
    btn_exit = Gtk.Template.Child()
    btn_logs = Gtk.Template.Child()
    log_box = Gtk.Template.Child()
    log_output = Gtk.Template.Child()

    def __init__(
        self,
        window,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.__window = window

        self.btn_logs.connect("clicked", self.__on_logs_clicked)
        self.btn_exit.connect("clicked", self.__on_exit_clicked)
        self.btn_tour.connect("clicked", self.__on_tour_clicked)

    def set_page_active(self):
        has_errors = len(backend.errors) > 0
        self.btn_logs.set_visible(has_errors)
        self.btn_tour.grab_focus()
    
    def set_page_inactive(self):
        return

    def __on_tour_clicked(self, *args):
        subprocess.Popen(["/usr/bin/vanilla-tour"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
        self.__window.close()

    def __on_exit_clicked(self, *args):
        self.__window.close()

    def __on_logs_clicked(self, *args):
        self.btn_logs.set_visible(False)
        self.log_box.set_visible(True)
        logs_text = "\n\n".join(backend.errors)
        self.log_output.set_label(logs_text)
