# timezone.py
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

_ = __builtins__["_"]

from gi.repository import Adw, Gtk

from vanilla_first_setup.views.locations import VanillaLocation

import vanilla_first_setup.core.timezones as tz
import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/timezone.ui")
class VanillaTimezone(Adw.Bin):
    __gtype_name__ = "VanillaTimezone"

    status_page = Gtk.Template.Child()
    footer = Gtk.Template.Child()
    current_timezone_label = Gtk.Template.Child()
    current_time_label = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        self.__location_page = VanillaLocation(window, _("Timezone"), tz.TimezonesDataSource())
        self.status_page.set_child(self.__location_page)

    def set_page_active(self):
        self.__location_page.set_page_active()

        selected_timezone = self.__location_page.selected_special
        if not selected_timezone:
            try:
                with open('/etc/timezone', 'r') as file:
                    selected_timezone = file.read().split("\n")[0]
            except Exception as e:
                print(e)

        if selected_timezone:
            time_string, with_date = tz.get_timezone_preview(selected_timezone)
            self.current_time_label.set_label(time_string)
            self.current_timezone_label.set_label(selected_timezone)

    def set_page_inactive(self):
        self.__location_page.set_page_inactive()

    def finish(self):
        self.__location_page.finish()
        timezone = self.__location_page.selected_special
        return backend.set_timezone(timezone)
