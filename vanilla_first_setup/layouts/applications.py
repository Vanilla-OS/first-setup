# applications.py
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

from gi.repository import Gtk, Adw

from vanilla_first_setup.dialog import VanillaDialog


@Gtk.Template(resource_path='/io/github/vanilla-os/FirstSetup/gtk/layout-applications.ui')
class VanillaLayoutApplications(Adw.Bin):
    __gtype_name__ = 'VanillaLayoutApplications'

    status_page = Gtk.Template.Child()
    bundles_list = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        self.__register_widgets = []
        self.__build_ui()

        # signals
        self.btn_next.connect("clicked", self.__next_step)

    def __build_ui(self):
        self.status_page.set_icon_name(self.__step["icon"])
        self.status_page.set_title(self.__step["title"])
        self.status_page.set_description(self.__step["description"])
        selection_dialogs = []

        def present_customize(widget, dialog):
                dialog.show()

        def close_customize(widget, dialog):
            dialog.hide()

        for item in self.__step["bundles"]:

            _selection_dialog = VanillaDialog(
                    self.__window,
                    "Select Applications",
                    "Description",
                )

            _cancel_button = Gtk.Button()
            _apply_button = Gtk.Button()
            _cancel_button.set_label("Cancel")
            _apply_button.set_label("Apply")
            _apply_button.add_css_class("suggested-action")

            _header_bar = Adw.HeaderBar()
            _header_bar.pack_start(_cancel_button)
            _header_bar.pack_end(_apply_button)
            _header_bar.set_show_end_title_buttons(False)
            _header_bar.set_show_start_title_buttons(False)

            _apps_list = Adw.PreferencesGroup()
            _apps_list.set_description("The following list includes only applications available in your preferred package manager.")
            _apps_page = Adw.PreferencesPage()
            _apps_page.add(_apps_list)

            _box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
            _box.append(_header_bar)
            _box.append(_apps_page)

            _selection_dialog.set_content(_box)
            _selection_dialog.set_default_size(500, 600)
            selection_dialogs.append(_selection_dialog)

            _action_row = Adw.ActionRow(
                title=item["title"],
                subtitle=item.get("subtitle", "")
            )
            _switcher = Gtk.Switch()
            _switcher.set_active(item.get("default", False))
            _switcher.set_valign(Gtk.Align.CENTER)
            _action_row.add_suffix(_switcher)

            _customize = Gtk.Button()
            _customize.set_icon_name("go-next-symbolic")
            _customize.set_valign(Gtk.Align.CENTER)
            _customize.add_css_class("flat")
            _action_row.add_suffix(_customize)

            _customize.connect("clicked", present_customize, selection_dialogs[-1])
            _cancel_button.connect("clicked", close_customize, selection_dialogs[-1])

            for app in item["applications"]:
                _apps_action_row = Adw.ActionRow(
                title=app["name"],
                icon_name=app["icon"]
                )
                _app_switcher = Gtk.Switch()
                _app_switcher.set_active(True)
                _app_switcher.set_valign(Gtk.Align.CENTER)
                _apps_action_row.add_suffix(_app_switcher)
                _apps_list.add(_apps_action_row)
            
            self.bundles_list.add(_action_row)

            self.__register_widgets.append((item["id"], _switcher))

            
    def __next_step(self, widget):
        self.__window.next()

    def get_finals(self):
        finals = {"vars": {}, "funcs": [x for x in self.__step["final"]]}

        for _id, switcher in self.__register_widgets:
            finals["vars"][_id] = switcher.get_active()

        return finals