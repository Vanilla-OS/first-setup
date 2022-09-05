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

from gi.repository import Gtk, Gio, Adw


@Gtk.Template(resource_path='/pm/mirko/UbuntuSmoother/gtk/window.ui')
class UbuntuSmootherWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'UbuntuSmootherWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
