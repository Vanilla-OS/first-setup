# applications_update.py
#
# Copyright 2023 mirkobrombin
# Copyright 2026 NN708
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
import hashlib
import subprocess

from gi.repository import Gtk, Adw
_ = __builtins__["_"]

import vanilla_first_setup.core.backend as backend
import vanilla_first_setup.core.applications as applications

class VanillaApplicationsDialogMixin:
    apps = {}
    category = ""

    finish_callback = None

    def on_apply_button_clicked(self, widget):
        self.set_visible(False)
        self.finish_callback(self.apps)

    def on_escape_key(self, action, callback=None):
        self.set_visible(False)
        self.finish_callback(self.apps)

    def build_apps(self):
        for app in self.apps[self.category]:
            apps_action_row = Adw.ActionRow(
                title=app["name"],
            )
            app_icon = Gtk.Image.new_from_icon_name(app["id"])
            app_icon.set_icon_size(Gtk.IconSize.LARGE)
            app_icon.add_css_class("lowres-icon")
            applications.set_app_icon_from_id_async(app_icon, app["id"])

            apps_action_row.add_prefix(app_icon)

            app_switch = Gtk.Switch()
            app_switch.set_active(True)
            if "active" in app:
                app_switch.set_active(app["active"])
            app_switch.set_valign(Gtk.Align.CENTER)
            app_switch.set_focusable(False)
            app_switch.connect("state-set", self.on_switch_state_change, app["id"])

            apps_action_row.add_suffix(app_switch)
            apps_action_row.set_activatable_widget(app_switch)

            self.applications_group.add(apps_action_row)

    def on_switch_state_change(self, widget, state, id):
        for app in self.apps[self.category]:
            if app["id"] == id:
                app["active"] = state
                break

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/applications-install-dialog.ui")
class VanillaApplicationsInstallDialog(Adw.Window, VanillaApplicationsDialogMixin):
    __gtype_name__ = "VanillaApplicationsInstallDialog"

    apply_button = Gtk.Template.Child()
    applications_group = Gtk.Template.Child()

    def __init__(self, window, apps, category: str, finish_callback, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)

        self.apps = copy.deepcopy(apps)
        self.category = category
        self.finish_callback = finish_callback

        self.apply_button.connect("clicked", self.on_apply_button_clicked)

        shortcut_controller = Gtk.ShortcutController.new()
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("Escape"), Gtk.CallbackAction.new(self.on_escape_key)
            )
        )
        self.add_controller(shortcut_controller)

        self.build_apps()
        self.set_visible(True)

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/applications-uninstall-dialog.ui")
class VanillaApplicationsUninstallDialog(Adw.Window, VanillaApplicationsDialogMixin):
    __gtype_name__ = "VanillaApplicationsUninstallDialog"

    apply_button = Gtk.Template.Child()
    applications_group = Gtk.Template.Child()

    def __init__(self, window, apps, category: str, finish_callback, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)

        self.apps = copy.deepcopy(apps)
        self.category = category
        self.finish_callback = finish_callback

        self.apply_button.connect("clicked", self.on_apply_button_clicked)

        shortcut_controller = Gtk.ShortcutController.new()
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("Escape"), Gtk.CallbackAction.new(self.on_escape_key)
            )
        )
        self.add_controller(shortcut_controller)

        self.build_apps()
        self.set_visible(True)

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/layout-applications-update.ui")
class VanillaLayoutApplicationsUpdate(Adw.Bin):
    __gtype_name__ = "VanillaLayoutApplicationsUpdate"

    bundles_list = Gtk.Template.Child()
    install_switch = Gtk.Template.Child()
    install_button = Gtk.Template.Child()
    uninstall_switch = Gtk.Template.Child()
    uninstall_button = Gtk.Template.Child()

    __apps = {
        "install": [],
        "uninstall": []
    }

    __already_setup_remote = False

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        apps_file_path = os.path.join(window.moduledir, "apps.json")
        with open(apps_file_path) as file:
            apps = json.load(file)
        with open(apps_file_path, "rb") as file:
            apps_file_digest = hashlib.file_digest(file, "sha256")

        seen_app_ids_file_path = os.path.join(os.path.expanduser('~'), ".local", "share", "vanilla-first-setup", "seen_app_ids.json")
        with open(seen_app_ids_file_path) as file:
            seen_app_ids = json.load(file)
        self.__seen_app_ids = {
            "apps_file_digest": apps_file_digest.hexdigest(),
            "install": seen_app_ids["install"] if "install" in seen_app_ids else [],
            "uninstall": seen_app_ids["uninstall"] if "uninstall" in seen_app_ids else []
        }

        result = subprocess.run("flatpak list --user --app --columns=application | jq -R . | jq -s .", shell=True, capture_output=True, text=True)
        installed_app_ids = json.loads(result.stdout)

        categories = ["core", "browsers", "utilities", "office"]
        for category in categories:
            for app in apps[category]:
                if app["id"] not in self.__seen_app_ids["install"]:
                    self.__seen_app_ids["install"].append(app["id"])
                    if app["id"] not in installed_app_ids:
                        self.__apps["install"].append(app)
        for app in apps["deprecated"]:
            if app["id"] not in self.__seen_app_ids["uninstall"]:
                self.__seen_app_ids["uninstall"].append(app["id"])
                if app["id"] in installed_app_ids:
                    self.__apps["uninstall"].append(app)

        self.install_switch.connect("state-set", self.__on_install_switch_state_change)
        self.uninstall_switch.connect("state-set", self.__on_uninstall_switch_state_change)

        self.install_button.connect("clicked", self.__on_customize_button_clicked, "install")
        self.uninstall_button.connect("clicked", self.__on_customize_button_clicked, "uninstall")

    def set_page_active(self):
        if not self.__already_setup_remote:
            success = backend.setup_flatpak_remote()
            self.__already_setup_remote = success
        self.__window.set_ready(True)
        self.__window.set_focus_on_next()

    def set_page_inactive(self):
        return

    def finish(self):
        backend.clear_flatpak_deferred()
        if self.install_switch.get_active():
            for app in self.__apps["install"]:
                if "active" not in app or app["active"]:
                    app_id = app["id"]
                    app_name = app["name"]
                    backend.install_flatpak_deferred(app_id, app_name)
        if self.uninstall_switch.get_active():
            for app in self.__apps["uninstall"]:
                if "active" not in app or app["active"]:
                    app_id = app["id"]
                    app_name = app["name"]
                    backend.uninstall_flatpak_deferred(app_id, app_name)

        backend.write_seen_app_ids_deferred(self.__seen_app_ids)
        return True


    def __on_install_switch_state_change(self, widget, state):
        self.install_button.set_sensitive(state)

    def __on_uninstall_switch_state_change(self, widget, state):
        self.uninstall_button.set_sensitive(state)

    def __on_customize_button_clicked(self, widget, app_type: str):
        dialog = None

        def update_apps(apps):
            self.__apps = apps
            dialog.destroy()
            return

        if app_type == "install":
            dialog = VanillaApplicationsInstallDialog(self.__window, self.__apps, app_type, update_apps)
        else:
            dialog = VanillaApplicationsUninstallDialog(self.__window, self.__apps, app_type, update_apps)
