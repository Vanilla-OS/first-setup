# done.py
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
from gi.repository import Gtk, Adw

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/logout.ui")
class VanillaLogout(Adw.Bin):
    __gtype_name__ = "VanillaLogout"

    status_page = Gtk.Template.Child()
    btn_login = Gtk.Template.Child()
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
        self.btn_login.connect("clicked", self.__on_login_clicked)

    def set_page_active(self):
        backend.remove_first_setup_user()
        has_errors = len(backend.errors) > 0
        self.btn_logs.set_visible(has_errors)
        self.btn_login.grab_focus()
    
    def set_page_inactive(self):
        return

    __already_subscribed = False
    __deferred_actions_succeeded = True
    __currently_running = False

    def __on_login_clicked(self, *args):
        if not self.__already_subscribed:
            backend.subscribe_progress(self.__deferred_progress_callback)
            self.__already_subscribed = True
        if not self.__currently_running:
            self.__currently_running = True
            backend.start_deferred_actions()
            self.__deferred_actions_succeeded = True

    def __deferred_progress_callback(self, id: str, uid: str, state: backend.ProgressState, info = None):
        if state == backend.ProgressState.Failed:
            self.__deferred_actions_succeeded = False
        if uid == "all_actions" and state == backend.ProgressState.Finished:
            self.__currently_running = False
            if self.__deferred_actions_succeeded:
                backend.logout()

    def __on_logs_clicked(self, *args):
        self.btn_logs.set_visible(False)
        self.log_box.set_visible(True)
        logs_text = "\n\n".join(backend.errors)
        self.log_output.set_label(logs_text)
