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

import time
from gi.repository import Gtk, Gdk, Gio, GLib, Vte, Pango

from vanilla_first_setup.utils.run_async import RunAsync

from vanilla_first_setup.views.tour import VanillaTour


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/progress.ui")
class VanillaProgress(Gtk.Box):
    __gtype_name__ = "VanillaProgress"

    carousel_tour = Gtk.Template.Child()
    tour_button = Gtk.Template.Child()
    tour_box = Gtk.Template.Child()
    progressbar = Gtk.Template.Child()
    console_button = Gtk.Template.Child()
    console_box = Gtk.Template.Child()
    console_output = Gtk.Template.Child()

    def __init__(self, window, tour: dict, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__tour = tour
        self.__success_fn = None
        self.__terminal = Vte.Terminal()
        self.__font = Pango.FontDescription()
        self.__font.set_family("Monospace")
        self.__font.set_size(13 * Pango.SCALE)
        self.__font.set_weight(Pango.Weight.NORMAL)
        self.__font.set_stretch(Pango.Stretch.NORMAL)
        self.__style_manager = self.__window.style_manager

        self.__build_ui()
        self.__on_setup_terminal_colors()

        self.__style_manager.connect("notify::dark", self.__on_setup_terminal_colors)
        self.tour_button.connect("clicked", self.__on_tour_button)
        self.console_button.connect("clicked", self.__on_console_button)

    def __on_setup_terminal_colors(self, *args):
          
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

    def __on_tour_button(self, *args):
        self.tour_box.set_visible(True)
        self.console_box.set_visible(False)
        self.tour_button.set_visible(False)
        self.console_button.set_visible(True)

    def __on_console_button(self, *args):
        self.tour_box.set_visible(False)
        self.console_box.set_visible(True)
        self.tour_button.set_visible(True)
        self.console_button.set_visible(False)

    def __build_ui(self):
        self.__terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__terminal.set_font(self.__font)
        self.__terminal.set_mouse_autohide(True)
        self.__terminal.set_input_enabled(False)
        self.console_output.append(self.__terminal)
        self.__terminal.connect("child-exited", self.on_vte_child_exited)

        for _, tour in self.__tour.items():
            self.carousel_tour.append(VanillaTour(self.__window, tour))

        self.__start_tour()

    def __switch_tour(self, *args):
        cur_index = self.carousel_tour.get_position() + 1
        if cur_index == self.carousel_tour.get_n_pages():
            cur_index = 0

        page = self.carousel_tour.get_nth_page(cur_index)

        self.carousel_tour.scroll_to(page, True)

    def __start_tour(self):
        def run_async():
            while True:
                GLib.idle_add(self.progressbar.pulse)
                GLib.idle_add(self.__switch_tour)
                time.sleep(5)

        RunAsync(run_async, None)

    def on_vte_child_exited(self, terminal, status, *args):
        terminal.get_parent().remove(terminal)
        status = not bool(status)

        if self.__success_fn is not None and status:
            self.__success_fn(*self.__success_fn_args)

        self.__window.set_installation_result(status, self.__terminal)

    def start(self, setup_commands, success_fn, *fn_args):
        self.__success_fn = success_fn
        self.__success_fn_args = fn_args

        self.__terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            ".",
            setup_commands,
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None,
        )
