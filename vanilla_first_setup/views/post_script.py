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

from gi.repository import Gtk, Gio, Gdk, GLib, Adw, Vte, Pango


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/post-script.ui")
class VanillaPostScript(Adw.Bin):
    __gtype_name__ = "VanillaPostScript"

    console_output = Gtk.Template.Child()

    def __init__(self, window, post_script: str, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__terminal = Vte.Terminal()
        self.__post_script = post_script
        self.__font = Pango.FontDescription()
        self.__font.set_family("Monospace")
        self.__font.set_size(13 * Pango.SCALE)
        self.__font.set_weight(Pango.Weight.NORMAL)
        self.__font.set_stretch(Pango.Stretch.NORMAL)
        self.__style_manager = self.__window.style_manager

        self.__build_ui()

        self.__style_manager.connect("notify::dark", self.__build_ui)

    def __build_ui(self, *args):
        self.__terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__terminal.set_font(self.__font)
        self.__terminal.set_mouse_autohide(True)

        self.console_output.append(self.__terminal)
        self.__terminal.connect("child-exited", self.on_vte_child_exited)

        is_dark: bool = self.__style_manager.get_dark()

        palette = [
            "#363636",
            "#c01c28",
            "#26a269",
            "#a2734c",
            "#12488b",
            "#a347ba",
            "#2aa1b3",
            "#cfcfcf",
            "#5d5d5d",
            "#f66151",
            "#33d17a",
            "#e9ad0c",
            "#2a7bde",
            "#c061cb",
            "#33c7de",
            "#ffffff",
        ]

        FOREGROUND = palette[0]
        BACKGROUND = palette[15]
        FOREGROUND_DARK = palette[15]
        BACKGROUND_DARK = palette[0]

        self.fg = Gdk.RGBA()
        self.bg = Gdk.RGBA()

        self.colors = [Gdk.RGBA() for c in palette]
        [color.parse(s) for (color, s) in zip(self.colors, palette)]
        
        if is_dark:
            self.fg.parse(FOREGROUND_DARK)
            self.bg.parse(BACKGROUND_DARK)
        else:
            self.fg.parse(FOREGROUND)
            self.bg.parse(BACKGROUND)
            
        self.__terminal.set_colors(self.fg, self.bg, self.colors)

        self.__terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["/bin/sh", "-c", self.__post_script],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None,
            None,
        )

    def on_vte_child_exited(self, terminal, status, *args):
        status = not bool(status)
        self.__window.next(result=status)
