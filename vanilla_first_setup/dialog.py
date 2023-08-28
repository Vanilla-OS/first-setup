# dialog.py
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

from gi.repository import Gtk, Adw


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/dialog.ui")
class VanillaDialog(Adw.Window):
    __gtype_name__ = "VanillaDialog"

    label_text = Gtk.Template.Child()

    def __init__(self, window, title, text, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        self.set_title(title)
        self.label_text.set_text(text)

        def hide(action, callback=None):
            self.hide()

        shortcut_controller = Gtk.ShortcutController.new()
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("Escape"), Gtk.CallbackAction.new(hide)
            )
        )
        self.add_controller(shortcut_controller)
