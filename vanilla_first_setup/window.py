# window.py
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

from gi.repository import Gtk, Adw, GLib

import vanilla_first_setup.core.backend as backend

from vanilla_first_setup.dialog import VanillaDialog

_ = __builtins__["_"]

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/window.ui")
class VanillaWindow(Adw.ApplicationWindow):
    __gtype_name__ = "VanillaWindow"

    stack = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    btn_next_spinner = Gtk.Template.Child()
    toasts = Gtk.Template.Child()
    style_manager = Adw.StyleManager().get_default()

    can_continue = False

    __is_finishing_step = False

    pages = []
    __current_page_index = 0

    def __init__(self, moduledir: str, configure_system_mode: bool, oem_mode: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.moduledir = moduledir
        self.configure_system_mode = configure_system_mode
        self.oem_mode = oem_mode

        self.__build_ui(configure_system_mode)
        self.__connect_signals()

        backend.subscribe_errors(self.__error_received)

    def set_ready(self, ready: bool = True):
        self.__loading_indicator(False)
        self.can_continue = ready
        self.btn_next.set_sensitive(ready)

    def finish_step(self):
        if not self.can_continue or self.__is_finishing_step:
            return
        self.can_continue = False
        self.__is_finishing_step = True
        
        self.__loading_indicator()
        
        thread = threading.Thread(target=self.__finish_step_thread)
        thread.start()

    def __error_received(self, script_name: str, command: list[str], id: int):
        GLib.idle_add(self.__error_toast, _("Setup failed: ") + script_name, id)

    def __error_toast(self, message: str, id: int):
        toast = Adw.Toast.new(message)
        toast.props.timeout = 0
        toast.props.button_label = _("Details")
        toast.connect("button-clicked", self.__error_toast_clicked, id)
        self.toasts.add_toast(toast)
    
    def __error_toast_clicked(self, widget, id: int):
        message = backend.errors[id]
        dialog = VanillaDialog(self, _("Error log"), message)
        dialog.present()

    def set_focus_on_next(self):
        self.btn_next.grab_focus()

    def __connect_signals(self):
        self.btn_back.connect("clicked", self.__on_btn_back_clicked)
        self.btn_next.connect("clicked", self.__on_btn_next_clicked)
        return

    def __build_ui(self, configure_system_mode: bool):

        if configure_system_mode:
            from vanilla_first_setup.views.welcome import VanillaWelcome
            if self.oem_mode:
                from vanilla_first_setup.views.language import VanillaLanguage
                from vanilla_first_setup.views.keyboard import VanillaKeyboard
                from vanilla_first_setup.views.timezone import VanillaTimezone
            from vanilla_first_setup.views.hostname import VanillaHostname
            from vanilla_first_setup.views.user import VanillaUser
            from vanilla_first_setup.views.logout import VanillaLogout

            self.__view_welcome = VanillaWelcome(self)
            self.__view_welcome.no_next_button = True
            self.__view_welcome.no_back_button = True
            if self.oem_mode:
                self.__view_language = VanillaLanguage(self)
                self.__view_language.no_back_button = True
                self.__view_keyboard = VanillaKeyboard(self)
                self.__view_timezone = VanillaTimezone(self)
                self.__view_hostname = VanillaHostname(self)
            else:
                self.__view_hostname = VanillaHostname(self)
                self.__view_hostname.no_back_button = True
            self.__view_user = VanillaUser(self)
            self.__view_logout = VanillaLogout(self)
            self.__view_logout.no_next_button = True

            self.pages.append(self.__view_welcome)
            if self.oem_mode:
                self.pages.append(self.__view_language)
                self.pages.append(self.__view_keyboard)
                self.pages.append(self.__view_timezone)
            self.pages.append(self.__view_hostname)
            self.pages.append(self.__view_user)
            self.pages.append(self.__view_logout)
        else:
            from vanilla_first_setup.views.welcome_user import VanillaWelcomeUser
            from vanilla_first_setup.views.conn_check import VanillaConnCheck
            from vanilla_first_setup.views.theme import VanillaTheme
            from vanilla_first_setup.views.applications import VanillaLayoutApplications
            from vanilla_first_setup.views.progress import VanillaProgress
            from vanilla_first_setup.views.done import VanillaDone

            self.__view_welcome = VanillaWelcomeUser(self)
            self.__view_welcome.no_next_button = True
            self.__view_welcome.no_back_button = True
            self.__view_conn_check = VanillaConnCheck(self)
            self.__view_conn_check.no_back_button = True
            self.__view_theme = VanillaTheme(self)
            self.__view_theme.no_back_button = True
            self.__view_apps = VanillaLayoutApplications(self)
            self.__view_progress = VanillaProgress(self)
            self.__view_progress.no_back_button = True
            self.__view_done = VanillaDone(self)
            self.__view_done.no_next_button = True

            self.pages.append(self.__view_welcome)
            self.pages.append(self.__view_conn_check)
            self.pages.append(self.__view_theme)
            self.pages.append(self.__view_apps)
            self.pages.append(self.__view_progress)
            self.pages.append(self.__view_done)

        for page in self.pages:
            self.stack.add_child(page)

        self.stack.set_visible_child(self.__view_welcome)

        self.__update_button_visibility(self.pages[0])
        self.__on_page_changed()

    def __on_page_changed(self, *args):
        current_page = self.stack.get_visible_child()
        current_page.set_page_active()
    
    def __on_btn_next_clicked(self, widget):
        self.finish_step()

    def __on_btn_back_clicked(self, widget):
        if self.__is_finishing_step:
            return
        self.__last_page()

    def __loading_indicator(self, waiting: bool = True):
        if self.__current_page_index == 0:
            self.btn_next.set_visible(False)
            self.btn_next_spinner.set_visible(False)
            return

        self.btn_next.set_visible(not waiting)
        self.btn_next_spinner.set_visible(waiting)

    def __finish_step_thread(self):
        success = self.stack.get_visible_child().finish()
        if success:
            GLib.idle_add(self.__next_page)
        else:
            GLib.idle_add(self.__fail)

    def __fail(self):
        self.__is_finishing_step = False
        self.__loading_indicator(False)
        self.set_ready(False)

    def __next_page(self):
        target_index = self.__current_page_index + 1
        self.__scroll_page(target_index)
        self.__is_finishing_step = False

    def __last_page(self):
        target_index = self.__current_page_index - 1
        self.__scroll_page(target_index)

    def __scroll_page(self, target_index: int):
        self.set_ready(False)

        old_current_page = self.stack.get_visible_child()
        target_page = self.pages[target_index]

        self.__update_button_visibility(target_page)

        self.stack.set_visible_child(target_page)
        self.__current_page_index = target_index

        old_current_page.set_page_inactive()
        self.__on_page_changed()

    def __update_button_visibility(self, current_page):
        no_back = getattr(current_page, "no_back_button", False)
        no_next = getattr(current_page, "no_next_button", False)

        self.btn_back.set_visible(not no_back)
        self.btn_next.set_visible(not no_next)

