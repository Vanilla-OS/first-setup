# progress.py
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
import vanilla_first_setup.core.backend as backend

from gi.repository import Gtk, Adw, GLib

_ = __builtins__["_"]

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/progress.ui")
class VanillaProgress(Adw.Bin):
    __gtype_name__ = "VanillaProgress"

    action_list = Gtk.Template.Child()

    actions = {}

    __not_started = True
    __finished = False
    __already_skipped = False
    __already_removed_autostart_file = False

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        self.__window = window

    def set_page_active(self):
        self.__window.set_ready(self.__finished)
        if self.__not_started:
            self.__not_started = False
            backend.subscribe_progress(self.__on_items_changed_thread)
            thread = threading.Thread(target=backend.start_deferred_actions)
            thread.start()

    def set_page_inactive(self):
        return

    def finish(self):
        if not self.__already_removed_autostart_file:
            self.__already_removed_autostart_file = backend.remove_autostart_file()
        return True
    
    def __on_items_changed_thread(self, id: str, uid: str, state: backend.ProgressState, info: dict):
        GLib.idle_add(self.__on_items_changed, id, uid, state, info)
    
    def __on_items_changed(self, id: str, uid: str, state: backend.ProgressState, info: dict):
        if id == "all_actions":
            if state == backend.ProgressState.Finished:
                self.__window.set_ready(True)
                self.__finished = True
                self.__skip_page_once()
            return

        if state == backend.ProgressState.Initialized:
            self.__add_new_action(id, uid, info)
            return

        status_suffix = None
        if state == backend.ProgressState.Running:
            status_suffix = Adw.Spinner()
        elif state == backend.ProgressState.Finished:
            status_suffix = Gtk.Image.new_from_icon_name("emblem-default-symbolic")
            status_suffix.add_css_class("success")
        elif state == backend.ProgressState.Failed:
            status_suffix = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
            status_suffix.add_css_class("error")

        if "suffix" in self.actions[uid]:
            self.actions[uid]["suffix"].set_visible(False)

        self.actions[uid]["widget"].add_suffix(status_suffix)
        self.actions[uid]["suffix"] = status_suffix

    def __add_new_action(self, id: str, uid: str, info: dict):
        title = ""
        icon = None
        if id == "setup_system":
            icon = Gtk.Image.new_from_icon_name("computer-symbolic")
            title = _("Setting up the system")
        elif id == "install_flatpak":
            icon = Gtk.Image.new_from_icon_name(info["app_id"])
            title = _("Installing") + " " + info["app_name"]
    
        row = Adw.ActionRow()
        row.set_title(title)
        icon.add_css_class("lowres-icon")
        icon.set_icon_size(Gtk.IconSize.LARGE)

        row.add_prefix(icon)

        self.action_list.add(row)
        self.actions[uid] = {"id": id, "info": info, "widget": row}

    def __skip_page_once(self):
        if not self.__already_skipped:
            self.__already_skipped = True
            self.__window.finish_step()
