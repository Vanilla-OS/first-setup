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

import os
import gi
import sys
import logging
from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Vte', '3.91')

from gi.repository import Gtk, Gdk, Gio, GLib, Adw, Vte, Pango
from vanilla_first_setup.window import VanillaWindow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FirstSetup::Main")


class FirstSetupApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.vanillaos.FirstSetup',
                flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.post_script = None
        self.user = os.environ.get("USER")
        self.new_user = False
        
        self.create_action('quit', self.close, ['<primary>q'])
        self.__register_arguments()

    def __register_arguments(self):
        """Register the command line arguments."""
        self.add_main_option(
            "run-post-script",
            ord("p"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            _("Run a post script"),
            None
        )
        self.add_main_option(
            "new-user",
            ord("p"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _("Run as a new user"),
            None
        )

    def do_command_line(self, command_line):
        """Handle command line arguments."""
        options = command_line.get_options_dict()

        if options.contains("run-post-script"):
            logger.info("Running post script")
            self.post_script = options.lookup_value("run-post-script").get_string()
            
        if options.contains("new-user"):
            logger.info("Running as a new user")
            self.user = None
            self.new_user = True

        self.activate()

    def do_activate(self):

    
        win = self.props.active_window
        if not win:
            win = VanillaWindow(application=self, post_script=self.post_script, user=self.user, new_user=self.new_user)
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
    if os.environ.get("USERNAME") in ["ubuntu", "vanillaos", "vanilla-os"]:
        logging.warning("Running in Live mode, closing...")
        sys.exit(0)

    app = FirstSetupApplication()
    return app.run(sys.argv)
