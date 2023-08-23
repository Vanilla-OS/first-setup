# network.py
#
# Copyright 2023 mirkobrombin
# Copyright 2023 matbme
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

from gi.repository import Gtk, Adw, NM


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/default-network.ui")
class VanillaDefaultNetwork(Adw.Bin):
    __gtype_name__ = "VanillaDefaultNetwork"

    wired_group = Gtk.Template.Child()
    wireless_group = Gtk.Template.Child()
    hidden_network_row = Gtk.Template.Child()
    proxy_settings_row = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step

        # self.__nm_client = NM.Client.new()
        # devices = self.__nm_client.get_devices()
        # for device in devices:
        #     if device.is_real():
        #         print(device.get_udi())

        # Since we have a dedicated page for checking connectivity,
        # we only need to make sure the user has some type of
        # connection set up, be it wired or wireless.
        self.has_some_connection = False

        self.set_next_btn_sensitive()

        self.btn_next.connect("clicked", self.__window.next)

    @property
    def step_id(self):
        return self.__key

    def get_finals(self):
        return {}

    def set_next_btn_sensitive(self):
        self.btn_next.add_css_class("suggested-action")
        self.btn_next.set_sensitive(True)
