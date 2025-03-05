# applications.py
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

import copy
import json
import os

from gi.repository import Gtk, Adw
_ = __builtins__["_"]

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/applications-dialog.ui")
class VanillaApplicationsDialog(Adw.Window):
    __gtype_name__ = "VanillaApplicationsDialog"

    apply_button = Gtk.Template.Child()
    applications_group = Gtk.Template.Child()

    __apps = {}
    __category = ""

    __finish_callback = None

    def __init__(self, window, apps, category: str, finish_callback, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        
        self.__apps = copy.deepcopy(apps)
        self.__category = category
        self.__finish_callback = finish_callback

        self.apply_button.connect("clicked", self.__on_apply_button_clicked)

        shortcut_controller = Gtk.ShortcutController.new()
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("Escape"), Gtk.CallbackAction.new(self.__on_escape_key)
            )
        )
        self.add_controller(shortcut_controller)

        self.__build_apps()
        self.set_visible(True)

    def __on_apply_button_clicked(self, widget):
        self.set_visible(False)
        self.__finish_callback(self.__apps)

    def __on_escape_key(self, action, callback=None):
        self.set_visible(False)
        self.__finish_callback(self.__apps)
    
    def __build_apps(self):
        for app in self.__apps[self.__category]:
            apps_action_row = Adw.ActionRow(
                title=app["name"],
            )
            app_icon = Gtk.Image.new_from_icon_name(app["id"])
            app_icon.set_icon_size(Gtk.IconSize.LARGE)
            app_icon.add_css_class("lowres-icon")

            apps_action_row.add_prefix(app_icon)

            app_switch = Gtk.Switch()
            app_switch.set_active(True)
            if "active" in app:
                app_switch.set_active(app["active"])
            app_switch.set_valign(Gtk.Align.CENTER)
            app_switch.set_focusable(False)
            app_switch.connect("state-set", self.__on_switch_state_change, app["id"])

            apps_action_row.add_suffix(app_switch)
            apps_action_row.set_activatable_widget(app_switch)

            self.applications_group.add(apps_action_row)
    
    def __on_switch_state_change(self, widget, state, id):
        for app in self.__apps[self.__category]:
            if app["id"] == id:
                app["active"] = state
                break

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/layout-applications.ui")
class VanillaLayoutApplications(Adw.Bin):
    __gtype_name__ = "VanillaLayoutApplications"

    bundles_list = Gtk.Template.Child()
    core_switch = Gtk.Template.Child()
    core_button = Gtk.Template.Child()
    browsers_switch = Gtk.Template.Child()
    browsers_button = Gtk.Template.Child()
    utilities_switch = Gtk.Template.Child()
    utilities_button = Gtk.Template.Child()
    office_switch = Gtk.Template.Child()
    office_button = Gtk.Template.Child()

    __apps = {}

    __already_setup_remote = False

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        apps_file_path = os.path.join(window.moduledir, "apps.json")
        with open(apps_file_path) as file:
            self.__apps = json.load(file)

        self.core_switch.connect("state-set", self.__on_core_switch_state_change)
        self.browsers_switch.connect("state-set", self.__on_browsers_switch_state_change)
        self.utilities_switch.connect("state-set", self.__on_utilities_switch_state_change)
        self.office_switch.connect("state-set", self.__on_office_switch_state_change)

        self.core_button.connect("clicked", self.__on_customize_button_clicked, "core")
        self.browsers_button.connect("clicked", self.__on_customize_button_clicked, "browsers")
        self.utilities_button.connect("clicked", self.__on_customize_button_clicked, "utilities")
        self.office_button.connect("clicked", self.__on_customize_button_clicked, "office")

    def set_page_active(self):
        if not self.__already_setup_remote:
            success = backend.setup_flatpak_remote()
            self.__already_setup_remote = success
        self.__window.set_ready(True)
        self.__window.set_focus_on_next()

    def set_page_inactive(self):
        return

    def finish(self):
        enabled_categories = []
        if self.core_switch.get_active():
            enabled_categories.append("core")
        if self.browsers_switch.get_active():
            enabled_categories.append("browsers")
        if self.utilities_switch.get_active():
            enabled_categories.append("utilities")
        if self.office_switch.get_active():
            enabled_categories.append("office")

        backend.clear_flatpak_deferred()
        for category in enabled_categories:
            for app in self.__apps[category]:
                if "active" not in app or app["active"]:
                    app_id = app["id"]
                    app_name = app["name"]
                    backend.install_flatpak_deferred(app_id, app_name)
        return True
        
    
    def __on_core_switch_state_change(self, widget, state):
        self.core_button.set_sensitive(state)

    def __on_browsers_switch_state_change(self, widget, state):
        self.browsers_button.set_sensitive(state)

    def __on_utilities_switch_state_change(self, widget, state):
        self.utilities_button.set_sensitive(state)

    def __on_office_switch_state_change(self, widget, state):
        self.office_button.set_sensitive(state)

    def __on_customize_button_clicked(self, widget, app_type: str):
        dialog = None

        def update_apps(apps):
            self.__apps = apps
            dialog.destroy()
            return

        dialog = VanillaApplicationsDialog(self.__window, self.__apps, app_type, update_apps)
