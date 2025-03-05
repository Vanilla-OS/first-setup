# locations.py
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
_ = __builtins__["_"]
import abc

from gi.repository import Adw, Gtk

import vanilla_first_setup.core.timezones as tz

logger = logging.getLogger("VanillaInstaller::Locations")

class LocationPageDataSource():
    @abc.abstractmethod
    def get_all_regions(self) -> list[str]:
        pass

    @abc.abstractmethod
    def find_name_for_region(self, region: str) -> str:
        pass

    @abc.abstractmethod
    def get_all_country_codes(self) -> list[str]:
        pass

    @abc.abstractmethod
    def get_all_country_codes_by_region(self, region: str) -> list[str]:
        pass

    @abc.abstractmethod
    def find_name_for_country_code(self, country_code: str) -> str:
        pass

    @abc.abstractmethod
    def get_specials_by_country_code(self, country_code: str) -> list[str]:
        pass

    @abc.abstractmethod
    def country_code_from_special(self, special: str) -> str:
        pass

    @abc.abstractmethod
    def region_from_special(self, special: str) -> str:
        pass

    @abc.abstractmethod
    def search_specials(self, search_term: str, max_results: int) -> tuple[list[str], bool]:
        '''should return a list of all specials which match search_term in some way 
        and a bool whether the list has been shortened due to max_results'''
        pass

    @abc.abstractmethod
    def find_name_for_special(self, special: str) -> str|None:
        pass

    @abc.abstractmethod
    def find_description_for_special(self, special: str) -> str|None:
        pass

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/widget-location-list-page.ui")
class VanillaLocationListPage(Adw.NavigationPage):
    __gtype_name__ = "VanillaLocationListPage"

    pref_group = Gtk.Template.Child()

    def __init__(self, title: str,
                 items: list[str],
                 display_names: list[str],
                 button_callback, active_items: list[str] = [],
                 suffixes: list[str]|None = None,
                 radio_buttons: bool = True,
                 **kwargs,
                 ):
        
        super().__init__(**kwargs)
        self.set_title(title)

        self.__items = items
        self.__button_callback = button_callback
        self.__display_names = display_names
        self.__suffixes = suffixes
        self.__active_items = active_items
        self.__radio_buttons = radio_buttons

        self.__buttons = []

        self.__build_ui()

    def update_active(self, items):
        self.__active_items = items

        for button, item in self.__buttons:
            is_active = item in self.__active_items
            button.set_active(is_active)

    def __build_ui(self):
        first_button = None

        for index, item in enumerate(self.__items):
            region_row = Adw.ActionRow()
            region_row.set_use_markup(False)
            region_row.set_title(self.__display_names[index])
            if self.__suffixes:
                label = Gtk.Label()
                label.set_label(self.__suffixes[index])
                region_row.add_suffix(label)

            button_active = item in self.__active_items
            button = self.__create_check_button(self.__on_button_activated, item, button_active)

            if self.__radio_buttons:
                if first_button:
                    button.set_group(first_button)
                else:
                    first_button = button

            region_row.add_prefix(button)
            region_row.set_activatable_widget(button)

            self.pref_group.add(region_row)
            self.__buttons.append((button, item))

    def __on_button_activated(self, widget, item):
        self.__button_callback(widget, item)
        self.update_active(self.__active_items)

    def __create_check_button(self, callback, item: str, active: bool) -> Gtk.CheckButton:
        button = Gtk.CheckButton()
        button.set_valign(Gtk.Align.CENTER)
        button.connect("activate", callback, item)
        button.set_focusable(False)
        button.set_active(active)

        return button

@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/location.ui")
class VanillaLocation(Adw.Bin):
    __gtype_name__ = "VanillaLocation"

    entry_search = Gtk.Template.Child()
    navigation = Gtk.Template.Child()
    search_warning_label = Gtk.Template.Child()
    
    selected_region = None
    selected_country_code = None
    selected_special = None

    def __init__(self, window, special_name: str, data_source: LocationPageDataSource, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__special_name = special_name
        self.__data_source = data_source

        self.navigation.connect("popped", self.__on_popped)
        self.entry_search.connect("search_changed", self.__on_search_field_changed)

    def set_page_active(self):
        if self.selected_special:
            self.__window.set_ready(True)

        if self.selected_region:
            self.__show_location(tz.user_region, tz.user_country_code)
        if tz.has_user_preferred_location():
            selected_region, selected_country_code = tz.get_user_preferred_location()
            if selected_region not in self.__data_source.get_all_regions():
                selected_region = ""
            if selected_country_code not in self.__data_source.get_all_country_codes():
                selected_country_code = ""
            self.__show_location(selected_region, selected_country_code)
        elif tz.user_region:
            user_region = tz.user_region
            user_country_code = tz.user_country_code
            if user_region not in self.__data_source.get_all_regions():
                user_region = ""
            if user_country_code not in self.__data_source.get_all_country_codes():
                user_country_code = ""
            self.__show_location(user_region, user_country_code)
        else:
            self.__show_location(None, None)

    def set_page_inactive(self):
        return

    def finish(self):
        tz.set_user_preferred_location(self.selected_region, self.selected_country_code)
        return

    def __show_location(self, region, country_code):
        stack = []
        regions_page = self.__build_ui()
        stack.append(regions_page)

        if region:
            country_page = self.__build_country_page(region)
            stack.append(country_page)
        
        if country_code:
            specials_page = self.__build_specials_page(country_code)
            stack.append(specials_page)

        self.navigation.replace(stack)
    
    def __build_ui(self) -> VanillaLocationListPage:
        regions = self.__data_source.get_all_regions()
        region_names = [self.__data_source.find_name_for_region(region) for region in self.__data_source.get_all_regions()]
        regions_page = VanillaLocationListPage(_("Region"),
                                               regions,
                                               region_names,
                                               self.__on_region_button_clicked,
                                               [self.selected_region],
                                               )
        regions_page.set_tag("region")

        return regions_page

    def __on_region_button_clicked(self, widget, region):
        country_page = self.__build_country_page(region)
        self.navigation.push(country_page)
    
    def __build_country_page(self, region) -> VanillaLocationListPage:
        country_codes = self.__data_source.get_all_country_codes_by_region(region)
        country_names = [self.__data_source.find_name_for_country_code(country_code) for country_code in country_codes]

        countries_page = VanillaLocationListPage(_("Country"),
                                                 country_codes,
                                                 country_names,
                                                 self.__on_country_button_clicked,
                                                 [self.selected_country_code],
                                                 )
        countries_page.set_tag("country")

        return countries_page

    def __on_country_button_clicked(self, widget, country_code):
        specials_page = self.__build_specials_page(country_code)
        self.navigation.push(specials_page)

    def __build_specials_page(self, country_code):

        specials = self.__data_source.get_specials_by_country_code(country_code)
        special_names = [self.__data_source.find_name_for_special(special) for special in specials]
        special_suffixes = [self.__data_source.find_description_for_special(special) for special in specials]

        specials_page = VanillaLocationListPage(self.__special_name,
                                                specials, special_names,
                                                self.__on_specials_button_clicked,
                                                [self.selected_special],
                                                special_suffixes,
                                                )
        specials_page.set_tag("special")

        return specials_page

    def __on_specials_button_clicked(self, widget, special):
        self.selected_country_code = self.__data_source.country_code_from_special(special)
        self.selected_region = self.__data_source.region_from_special(special)
        self.selected_special = special
        self.__refresh_activated_buttons()
        self.__window.set_ready()
        self.__window.finish_step()

    def __on_popped(self, nag_view, page):
        if page.get_tag() == "search":
            self.search_warning_label.set_visible(False)

    def __refresh_activated_buttons(self):
        region_page = self.navigation.find_page("region")
        if region_page:
            region_page.update_active([self.selected_region])

        country_page = self.navigation.find_page("country")
        if country_page:
            country_page.update_active([self.selected_country_code])

        specials_page = self.navigation.find_page("special")
        if specials_page:
            specials_page.update_active([self.selected_special])

        search_page = self.navigation.find_page("search")
        if search_page:
            search_page.update_active([self.selected_special])

    def __retrieve_navigation_stack(self) -> list[VanillaLocationListPage]:
        stack = []

        page = self.navigation.get_visible_page()
        while page:
            stack.insert(0, page)
            page = self.navigation.get_previous_page(page)

        return stack

    def __on_search_field_changed(self, *args):
        max_results = 50

        search_term: str = self.entry_search.get_text().strip()

        if not search_term:
            nav_page = self.navigation.get_visible_page()
            if nav_page and nav_page.get_tag() == "search":
                self.navigation.pop()
            return

        specials_filtered, list_shortened = self.__data_source.search_specials(search_term, max_results)

        if len(specials_filtered) > max_results:
            list_shortened = True
            specials_filtered = specials_filtered[0:max_results]

        special_names_filtered = [self.__data_source.find_name_for_special(special) for special in specials_filtered]
        special_suffixes = [self.__data_source.find_description_for_special(special) for special in specials_filtered]

        new_search_nav_page = VanillaLocationListPage(_("Search results"),
                                                      specials_filtered,
                                                      special_names_filtered,
                                                      self.__on_specials_button_clicked,
                                                      [self.selected_special],
                                                      special_suffixes,
                                                      )
        new_search_nav_page.set_tag("search")

        if self.navigation.get_visible_page().get_tag() == "search":
            stack = self.__retrieve_navigation_stack()
            stack.pop()
            stack.append(new_search_nav_page)
            self.navigation.replace(stack)
        else:
            self.navigation.push(new_search_nav_page)

        self.search_warning_label.set_visible(list_shortened)
