# window.py
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

import time
from gi.repository import Gtk, Gio, GLib, Adw

from vanilla_first_setup.models.preset import Preset
from vanilla_first_setup.models.config import Config
from vanilla_first_setup.utils.processor import Processor
from vanilla_first_setup.utils.run_async import RunAsync
from vanilla_first_setup.utils.configurator import Configurator
from vanilla_first_setup.utils.welcome_langs import welcome
from vanilla_first_setup.utils.checks import has_nvidia_gpu
from vanilla_first_setup.dialogs.subsystem import SubSystemDialog
from vanilla_first_setup.dialogs.prop_drivers import ProprietaryDriverDialog


@Gtk.Template(resource_path='/io/github/vanilla-os/FirstSetup/gtk/window.ui')
class FirstSetupWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FirstSetupWindow'

    carousel = Gtk.Template.Child()
    btn_go_theme = Gtk.Template.Child()
    btn_light = Gtk.Template.Child()
    btn_dark = Gtk.Template.Child()
    btn_go_package = Gtk.Template.Child()
    btn_go_subsystem = Gtk.Template.Child()
    btn_save = Gtk.Template.Child()
    btn_reboot = Gtk.Template.Child()
    btn_no_subsystem = Gtk.Template.Child()
    btn_use_subsystem = Gtk.Template.Child()
    btn_info_subsystem = Gtk.Template.Child()
    btn_no_prop_nvidia = Gtk.Template.Child()
    btn_use_prop_nvidia = Gtk.Template.Child()
    btn_info_prop_nvidia = Gtk.Template.Child()
    switch_snap = Gtk.Template.Child()
    switch_flatpak = Gtk.Template.Child()
    switch_appimage = Gtk.Template.Child()
    switch_apport = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    status_welcome = Gtk.Template.Child()
    status_nvidia = Gtk.Template.Child()

    page_welcome = -1
    page_theme = 0
    page_configuration = 1
    page_subsystem = 2
    page_nvidia_drivers = 3
    page_extras = 4
    page_progress = 5
    page_done = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__config = Config(
            snap=Preset.snap,
            flatpak=Preset.flatpak,
            appimage=Preset.appimage,
            apport=Preset.apport,
            apx=Preset.apx,
            nvidia=Preset.nvidia,
        )
        self.__has_nvidia = has_nvidia_gpu()
        self.__buiild_ui()
        self.__connect_signals()
        self.__start_welcome_animation()

    def __buiild_ui(self):
        if self.__has_nvidia:
            self.status_nvidia.set_visible(True)

        self.switch_snap.set_active(Preset.snap)
        self.switch_flatpak.set_active(Preset.flatpak)
        self.switch_appimage.set_active(Preset.appimage)
        self.switch_apport.set_active(Preset.apport)

        self.btn_dark.set_group(self.btn_light)

    def __connect_signals(self):
        # go to pages
        self.btn_go_theme.connect('clicked', self.__show_page, self.page_theme)
        self.btn_go_package.connect('clicked', self.__show_page, self.page_configuration)
        self.btn_go_subsystem.connect('clicked', self.__show_page, self.page_subsystem)

        # save
        self.btn_save.connect('clicked', self.__on_btn_save_clicked)

        # reboot
        self.btn_reboot.connect('clicked', self.__on_btn_reboot_clicked)

        # theme
        self.btn_light.connect('toggled', self.__set_theme, "light")
        self.btn_dark.connect('toggled', self.__set_theme, "dark")

        # subsystem
        self.btn_no_subsystem.connect('clicked', self.__on_btn_subsystem_clicked, False)
        self.btn_use_subsystem.connect('clicked', self.__on_btn_subsystem_clicked, True)
        self.btn_info_subsystem.connect('clicked', self.__on_btn_info_subsystem_clicked)

        # nvidia
        self.btn_no_prop_nvidia.connect('clicked', self.__on_btn_prop_nvidia_clicked, False)
        self.btn_use_prop_nvidia.connect('clicked', self.__on_btn_prop_nvidia_clicked, True)
        self.btn_info_prop_nvidia.connect('clicked', self.__on_btn_info_prop_nvidia_clicked)

        # snap
        self.switch_snap.connect('state-set', self.__on_switch_snap_state_set)

        # flatpak
        self.switch_flatpak.connect('state-set', self.__on_switch_flatpak_state_set)

        # appimage
        self.switch_appimage.connect('state-set', self.__on_switch_appimage_state_set)

        # apport
        self.switch_apport.connect('state-set', self.__on_switch_apport_state_set)

    def __show_page(self, widget=None, page: int=-1):
        _page = self.carousel.get_nth_page(page + 1)
        self.carousel.scroll_to(_page, True)
    
    def __on_btn_save_clicked(self, widget):
        def __on_done(result, error=None):
            self.spinner.stop()
            self.__show_page(page=self.page_done)

        self.__show_page(page=self.page_progress)
        self.spinner.start()

        RunAsync(Processor(self.__config).run, __on_done)
    
    def __set_theme(self, widget, theme: str):
        self.__config.set_val('theme', theme)
        pref = "prefer-dark" if theme == "dark" else "default"
        gtk = "Adwaita-dark" if theme == "dark" else "Adwaita"
        Gio.Settings.new("org.gnome.desktop.interface").set_string("color-scheme", pref)
        Gio.Settings.new("org.gnome.desktop.interface").set_string("gtk-theme", gtk)

    def __on_switch_snap_state_set(self, widget, state):
        self.__config.set_val('snap', state)

    def __on_switch_flatpak_state_set(self, widget, state):
        self.__config.set_val('flatpak', state)

    def __on_switch_appimage_state_set(self, widget, state):
        self.__config.set_val('appimage', state)

    def __on_switch_apport_state_set(self, widget, state):
        self.__config.set_val('apport', state)

    def __on_switch_apx_state_set(self, widget, state):
        self.__config.set_val('apx', state)

    def __on_btn_reboot_clicked(self, widget):
        Configurator.reboot()

    def __on_btn_subsystem_clicked(self, widget, state):
        self.__config.set_val('apx', state)
        self.__show_page(page=self.page_nvidia_drivers if self.__has_nvidia else self.page_extras)

        if not self.__has_nvidia:
            self.__on_btn_save_clicked()
    
    def __on_btn_info_subsystem_clicked(self, widget):
        SubSystemDialog(self).show()
    
    def __on_btn_prop_nvidia_clicked(self, widget, state):
        self.__config.set_val('nvidia', state)
        self.__show_page(page=self.page_extras)

    def __on_btn_info_prop_nvidia_clicked(self, widget):
        ProprietaryDriverDialog(self).show()

    def __start_welcome_animation(self):
        def change_langs():
            for lang in welcome:
                GLib.idle_add(self.status_welcome.set_title, lang )
                time.sleep(1.5)

        RunAsync(change_langs, None)