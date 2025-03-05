# welcome.py
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
import threading
import random

from gi.repository import Gtk, GLib, Adw

import vanilla_first_setup.core.backend as backend

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/welcome.ui")
class VanillaWelcome(Adw.Bin):
    __gtype_name__ = "VanillaWelcome"

    btn_next = Gtk.Template.Child()
    btn_access = Gtk.Template.Child()
    title_label = Gtk.Template.Child()

    __stop_animation = True

    welcome = [
        "Welcome",
        "Benvenuto",
        "Bienvenido",
        "Bienvenue",
        "Willkommen",
        "Bem-vindo",
        "Добро пожаловать",
        "欢迎",
        "ようこそ",
        "환영합니다",
        "أهلا بك",
        "ברוך הבא",
        "Καλώς ήρθατε",
        "Hoşgeldiniz",
        "Welkom",
        "Witamy",
        "Välkommen",
        "Tervetuloa",
        "Vítejte",
        "Üdvözöljük",
        "Bun venit",
        "Vitajte",
        "Tere tulemast",
        "Sveiki atvykę",
        "Dobrodošli",
        "خوش آمدید",
        "आपका स्वागत है",
        "স্বাগতম",
        "வரவேற்கிறோம்",
        "స్వాగతం",
        "मुबारक हो",
        "સુસ્વાગત છે",
        "ಸುಸ್ವಾಗತ",
        "സ്വാഗതം",
    ]
    current_welcome_text = 0

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window

        random.shuffle(self.welcome)

        self.btn_next.connect("clicked", self.__on_btn_next_clicked)
        self.btn_access.connect("clicked", self.__on_btn_access_clicked)

    def set_page_active(self):
        self.__window.set_ready(True)
        self.btn_next.grab_focus()

        self.__stop_animation = False
        self.__start_welcome_animation()

    def set_page_inactive(self):
        self.__stop_animation = True

    def finish(self):
        return True

    def __start_welcome_animation(self):
        def change_langs_thread():
            while not self.__stop_animation:
                time.sleep(1.2)
                lang = self.welcome[self.current_welcome_text]
                GLib.idle_add(self.title_label.set_text, lang)

                self.current_welcome_text += 1
                if self.current_welcome_text > len(self.welcome)-1:
                    self.current_welcome_text = 0

        welcome_animation_thread = threading.Thread(target=change_langs_thread)
        welcome_animation_thread.start()

    def __on_btn_next_clicked(self, widget):
        self.__window.finish_step()

    def __on_btn_access_clicked(self, widget):
        thread = threading.Thread(target=backend.open_accessibility_settings)
        thread.start()
