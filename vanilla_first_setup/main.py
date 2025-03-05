# main.py
#
# Copyright 2025 mirkobrombin
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
import os
import signal
import locale
import gettext

from gi.repository import Gio

def main(version, moduledir: str, localedir: str):
    """The application's entry point."""
    if moduledir == "":
        print("Can't continue without a data directory.")
        sys.exit(1)
        return
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    locale.bindtextdomain('vanilla-first-setup', localedir)
    locale.textdomain('vanilla-first-setup')
    gettext.install('vanilla-first-setup', localedir)

    resource = Gio.Resource.load(os.path.join(moduledir, 'vanilla-first-setup.gresource'))
    resource._register()

    import vanilla_first_setup.core.backend as backend
    from vanilla_first_setup.application import FirstSetupApplication

    backend.set_script_path(os.path.join(moduledir, "scripts"))
    app = FirstSetupApplication(moduledir)
    return app.run(sys.argv)
