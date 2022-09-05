# main.py
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

import sys
import gi
import logging

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw

from ubuntu_smoother.window import UbuntuSmootherWindow


logging.basicConfig(level=logging.INFO)


class UbuntuSmootherApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='pm.mirko.UbuntuSmoother',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.close, ['<primary>q'])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = UbuntuSmootherWindow(application=self)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    
    def close(self, *args):
        """Close the application."""
        self.quit()


def main(version):
    """The application's entry point."""
    app = UbuntuSmootherApplication()
    return app.run(sys.argv)