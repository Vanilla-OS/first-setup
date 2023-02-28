# conn_check.py
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

from urllib.request import urlopen
from urllib.error import URLError
import os

from gi.repository import Gtk, GLib, Adw

from vanilla_first_setup.utils.run_async import RunAsync


@Gtk.Template(resource_path='/io/github/vanilla-os/FirstSetup/gtk/default-conn-check.ui')
class VanillaDefaultConnCheck(Adw.Bin):
    __gtype_name__ = 'VanillaDefaultConnCheck'

    btn_recheck = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step

        # connection check start
        self.__start_conn_check()

        # signals
        self.btn_recheck.connect("clicked", self.__on_btn_recheck_clicked)

    @property
    def step_id(self):
        return self.__key

    def get_finals(self):
        return {}

    def __start_conn_check(self):
        def async_fn():
            if "VANILLA_SKIP_CONN_CHECK" in os.environ:
                return True

            try:
                urlopen("https://google.com", timeout=1)
                return True
            except:
                return False

        def callback(res, *args):
            if res:
                self.__window.next()
                return

            self.status_page.set_icon_name("network-wired-disconnected-symbolic")
            self.status_page.set_title(_("No Internet Connection!"))
            self.status_page.set_description(_("First Setup requires an active internet connection"))
            self.btn_recheck.set_visible(True)

        RunAsync(async_fn, callback)

    def __on_btn_recheck_clicked(self, widget, *args):
        widget.set_visible(False)
        self.status_page.set_icon_name("content-loading-symbolic")
        self.status_page.set_title(_("Checking Connection…"))
        self.status_page.set_description(_("Please wait until the connection check is done."))
        self.__start_conn_check()
