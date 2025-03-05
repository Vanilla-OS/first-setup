# theme.py
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

import logging

from gi.repository import Gtk, Gio, Adw, GdkPixbuf

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/theme.ui")
class VanillaTheme(Adw.Bin):
    __gtype_name__ = "VanillaTheme"

    default_image = Gtk.Template.Child()
    dark_image = Gtk.Template.Child()
    btn_default = Gtk.Template.Child()
    btn_dark = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__style_manager = self.__window.style_manager

        self.btn_default.set_active(not self.__style_manager.get_dark())
        self.btn_dark.set_active(self.__style_manager.get_dark())

        self.__set_wallpaper_assets()

        self.btn_default.connect("toggled", self.__set_theme, "light")
        self.btn_dark.connect("toggled", self.__set_theme, "dark")

    def set_page_active(self):
        self.__window.set_ready()
        self.__window.set_focus_on_next()

    def set_page_inactive(self):
        return

    def finish(self):
        return True

    def __set_theme(self, widget, theme: str):
        if widget.get_active():
            backend.set_theme(theme)

    def __set_wallpaper_assets(self):
        wallpaper_schema = Gio.Settings.new("org.gnome.desktop.background")

        try:
            default_pixbuf = GdkPixbuf.Pixbuf.new_from_file(wallpaper_schema.get_string("picture-uri").split("file://")[1])
            dark_pixbuf = GdkPixbuf.Pixbuf.new_from_file(wallpaper_schema.get_string("picture-uri-dark").split("file://")[1])
        except:
            default_pixbuf = GdkPixbuf.Pixbuf.new_from_resource("/org/vanillaos/FirstSetup/assets/background_replacement.png")
            dark_pixbuf = default_pixbuf
            logging.warning("could not load background, falling back to replacement image")

        self.default_image.set_pixbuf(default_pixbuf.scale_simple(180, 120, GdkPixbuf.InterpType.BILINEAR))
        self.dark_image.set_pixbuf(dark_pixbuf.scale_simple(180, 120, GdkPixbuf.InterpType.BILINEAR))
