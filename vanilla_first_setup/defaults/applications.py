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
        self.__window.connect("page-changed", self.__on_page_changed)

    @property
    def step_id(self):
        return self.__key

    def __build_ui(self):
        self.status_page.set_icon_name(self.__step["icon"])
        self.status_page.set_title(self.__step["title"])
        self.status_page.set_description(self.__step["description"])
        selection_dialogs = []
        _index = 0

        def present_customize(widget, dialog, apps_list, item):
            for app in item["applications"]:
                try:
                    apps_list.remove(app["apps_action_row"])
                except KeyError:
                    pass
                if self.__window.builder.get_temp_finals("packages")["vars"]["flatpak"] == True:
                    package_manager = "flatpak"
                elif self.__window.builder.get_temp_finals("packages")["vars"]["snap"] == True:
                    try:
                        package_manager = "snap"
                    except KeyError:
                        continue
                else:
                    continue
                try:
                    if app[package_manager]:
                        _apps_action_row = Adw.ActionRow(
                            title=app["name"],
                        )
                        _app_icon = Gtk.Image.new_from_resource("/io/github/vanilla-os/FirstSetup/assets/bundle-app-icons/" + app["icon"] + ".png")
                        _app_icon.set_icon_size(Gtk.IconSize.LARGE)
                        _app_icon.add_css_class("lowres-icon")
                        _apps_action_row.add_prefix(_app_icon)
                        _app_switcher = Gtk.Switch()
                        _app_switcher.set_active(True)
                        _app_switcher.set_valign(Gtk.Align.CENTER)
                        _apps_action_row.add_suffix(_app_switcher)
                        apps_list.add(_apps_action_row)
                        app["apps_action_row"] = _apps_action_row
                        app["switch"] = _app_switcher
                        try:
                            app["switch"].set_active(app["active"])
                        except KeyError:
                            pass
                except KeyError:
                    continue
            dialog.show()

        def close_customize(widget, dialog):
            dialog.hide()

        def apply_preferences(widget, dialog, apps_list, item):
            for app in item["applications"]:
                app["active"] = app["switch"].get_active()
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

            _customize.connect("clicked", present_customize, selection_dialogs[-1], _apps_list, item)
            _cancel_button.connect("clicked", close_customize, selection_dialogs[-1])
            _apply_button.connect("clicked", apply_preferences, selection_dialogs[-1], _apps_list, item)

            self.bundles_list.add(_action_row)

            self.__register_widgets.append((item["id"], _switcher, _index))
            _index += 1

    def __on_page_changed(self, widget, page):
        if page == self.__key:
            if True not in [
                self.__window.builder.get_temp_finals("packages")["vars"]["flatpak"],
                self.__window.builder.get_temp_finals("packages")["vars"]["snap"]
            ]:
                self.bundles_list.set_sensitive(False)
            else:
                self.bundles_list.set_sensitive(True)

    def __next_step(self, *args):
        self.__window.next()

    def get_finals(self):
        finals = {"vars": {}, "funcs": [x for x in self.__step["final"]]}

        if self.__window.builder.get_temp_finals("packages")["vars"]["flatpak"] == True:
            package_manager = "flatpak"
        elif self.__window.builder.get_temp_finals("packages")["vars"]["snap"] == True:
            try:
                package_manager = "snap"
            except KeyError:
                package_manager = None
        else:
            package_manager = None

        for _id, switcher, index in self.__register_widgets:
            if switcher.get_active() == True:
                for app in self.__step["bundles"][index]["applications"]:
                    if package_manager not in app.keys():
                        app["active"] = False
                    if "active" not in app.keys():
                        app["active"] = True
                    finals["vars"][app["name"]] = app["active"]
            else:
                for app in self.__step["bundles"][index]["applications"]:
                    finals["vars"][app["name"]] = False

        return finals
