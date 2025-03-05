# conn_check.py
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

import threading
import logging
_ = __builtins__["_"]

from gi.repository import Adw, Gtk, Gio, GLib

import vanilla_first_setup.core.backend as backend

logger = logging.getLogger("FirstSetup::Conn_Check")


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/conn-check.ui")
class VanillaConnCheck(Adw.Bin):
    __gtype_name__ = "VanillaConnCheck"

    status_page = Gtk.Template.Child()
    btn_settings = Gtk.Template.Child()

    __network_monitor = None
    __active = False
    __already_skipped = False

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        self.__network_monitor = Gio.NetworkMonitor.get_default()

        self.__network_monitor.connect("network-changed", self.__check_network_status)
        self.btn_settings.connect("clicked", self.__on_btn_settings_clicked)

    def set_page_active(self):
        self.__active = True
        self.__check_network_status()

    def set_page_inactive(self):
        self.__active = False

    def finish(self):
        return True

    def __check_network_status(self, *args):
        if not self.__active:
            return
        
        if self.__network_monitor.get_connectivity() == Gio.NetworkConnectivity.FULL:
            self.__set_network_connected()
            self.__window.set_ready(True)
        else:
            self.__set_network_disconnected()
            self.__window.set_ready(False)

    def __set_network_disconnected(self):
        logger.info("Internet connection available.")
        self.status_page.set_icon_name("network-wired-disconnected-symbolic")
        self.status_page.set_title(_("No Internet Connection!"))
        self.status_page.set_description(_("First Setup requires an active internet connection"))
        self.btn_settings.set_visible(True)

    def __set_network_connected(self):
        logger.info("Internet connection not avaiable.")
        self.status_page.set_icon_name("emblem-default-symbolic")
        self.status_page.set_title(_("Connection available"))
        self.status_page.set_description(_("You have a working internet connection"))
        self.btn_settings.set_visible(False)
        if not self.__already_skipped:
            self.__already_skipped = True
            GLib.idle_add(self.__window.finish_step)

    def __on_btn_settings_clicked(self, widget):
        thread = threading.Thread(target=backend.open_network_settings)
        thread.start()
        return
