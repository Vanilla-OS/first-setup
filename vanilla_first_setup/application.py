# application.py
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


import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gdk, Gio, GLib, Adw

import os
import sys
import logging
import grp
_ = __builtins__["_"]
from vanilla_first_setup.window import VanillaWindow
import vanilla_first_setup.core.backend as backend

logger = logging.getLogger("FirstSetup::Main")

class FirstSetupApplication(Adw.Application):
    """The main application singleton class."""

    moduledir = ""

    def __init__(self, moduledir: str, *args, **kwargs):

        log_path = "/tmp/first-setup.log"

        self.moduledir = moduledir

        if not os.path.exists(log_path):
            try:
                open(log_path, "a").close()
                os.chmod(log_path, 0o666)
                logging.basicConfig(level=logging.DEBUG,
                            filename=log_path,
                            filemode='a',
                            )
            except OSError as e:
                logger.warning(f"failed to create log file: {log_path}: {e}")
                logging.warning("No log will be stored.")


        super().__init__(
            *args,
            application_id="org.vanillaos.FirstSetup",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )
        self.dry_run = True

        self.__register_arguments()

    def __register_arguments(self):
        """Register the command line arguments."""
        self.add_main_option(
            "dry-run",
            ord("d"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _("Don't make any changes to the system."),
            None,
        )
        self.add_main_option(
            "force-configure-mode",
            ord("c"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _("Force the configure system mode, independant of group."),
            None,
        )
        self.add_main_option(
            "force-regular-mode",
            ord("r"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _("Force the regular mode, independant of group."),
            None,
        )
        self.add_main_option(
            "oem-mode",
            ord("o"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            _("Use the original equipment manufacturer mode with language, keyboard and timezone selection."),
            None,
        )

    def do_command_line(self, command_line):
        """Handle command line arguments."""
        options = command_line.get_options_dict()

        if options.lookup_value("dry-run"):
            logger.info("Running in dry-run mode.")
            self.dry_run = True
        else:
            self.dry_run = False
        
        self.force_configure = bool(options.lookup_value("force-configure-mode"))
        self.force_regular = bool(options.lookup_value("force-regular-mode"))
        self.oem_mode = bool(options.lookup_value("oem-mode"))
        
        backend.set_dry_run(self.dry_run)
            
        self.activate()
        return 0

    def do_activate(self):
        """
        Called when the application is activated.
        We raise the application's main window, creating it if
        necessary.
        """
        all_groups = [g.gr_name for g in grp.getgrall()]
        configure_system_mode = False
        if "vanilla-first-setup" in all_groups and os.getlogin() in grp.getgrnam("vanilla-first-setup").gr_mem:
            configure_system_mode = True

        if self.force_configure:
            configure_system_mode = True
        elif self.force_regular:
            configure_system_mode = False

        if configure_system_mode:
            print("Running in configure system mode.")
            backend.disable_lockscreen()
        else:
            print("Running in regular mode.")
            backend.setup_system_deferred()

        provider = Gtk.CssProvider()
        provider.load_from_resource("/org/vanillaos/FirstSetup/style.css")
        Gtk.StyleContext.add_provider_for_display(
            display=Gdk.Display.get_default(),
            provider=provider,
            priority=Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        win = self.props.active_window
        if not win:
            win = VanillaWindow(
                application=self,
                moduledir=self.moduledir,
                configure_system_mode=configure_system_mode,
                oem_mode=self.oem_mode,
            )
        win.present()

    def close(self, *args):
        """Close the application."""
        self.quit()

