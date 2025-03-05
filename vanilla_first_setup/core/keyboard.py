import logging
import copy

import gi
gi.require_version("GnomeDesktop", "4.0")
from gi.repository import GnomeDesktop

import vanilla_first_setup.core.timezones as tz

logger = logging.getLogger("FirstSetup::Keyboard")

xkb = GnomeDesktop.XkbInfo()

all_regions: list[str] = []
all_region_names: list[str] = []
all_country_codes: list[str] = []
all_country_codes_by_region: dict[str, list[str]] = {}
all_keyboard_layouts: list[str] = []
all_keyboard_layout_names: list[str] = []
all_keyboard_layouts_by_country_code: dict[str, list[str]] = {}
all_keyboard_layout_names_by_country_code: dict[str, list[str]] = {}

def region_from_keyboard(keyboard) -> str:
    return tz.region_from_country_code(country_code_from_keyboard(keyboard))
        
def country_code_from_keyboard(keyboard) -> str:
    for country_code, e_keyboards in all_keyboard_layouts_by_country_code.items():
        for e_keyboard in e_keyboards:
            if keyboard == e_keyboard:
                return country_code
    return ""

def retrieve_country_names_by_region(region) -> list[str]:
    country_codes = all_country_codes_by_region[region]
    countries = copy.deepcopy(country_codes)
    for idx, country_code in enumerate(countries):
        countries[idx] = tz.all_country_names_by_code[country_code]
    return countries

def search_keyboards(search_term: str, limit: int) -> tuple[list[str], bool]:
    '''
        search_keyboards looks for all keyboard names with substring search_term

        search is not case sensitive
    
        returns a list of all matching keyboard names and a bool if the list is shortened due to the limit
    '''
    clean_search_term = search_term.lower()

    keyboards_filtered = []
    list_shortened = False
    for index, keyboard_layout_name in enumerate(all_keyboard_layout_names):
        if len(keyboards_filtered) >= limit:
            list_shortened = True
            break
        does_match = True
        for search_term_part in clean_search_term.split(" "):
            if search_term_part not in keyboard_layout_name.lower():
                does_match = False
        if does_match:
            keyboards_filtered.append(all_keyboard_layouts[index])
    return (keyboards_filtered, list_shortened)

def find_keyboard_layout_name_for_keyboard(keyboard: str) -> str:
    index = all_keyboard_layouts.index(keyboard)
    return all_keyboard_layout_names[index]

def is_variant_of_same_layout(keyboard_layout_a: str, keyboard_layout_b: str) -> bool:
    info_a = xkb.get_layout_info(keyboard_layout_a)
    info_b = xkb.get_layout_info(keyboard_layout_b)

    same_layout = info_a.xkb_layout == info_b.xkb_layout
    return same_layout
    
for country_code in tz.all_country_codes:
    layouts = xkb.get_layouts_for_country(country_code)
    layouts.sort(key=len)

    if len(layouts) == 0:
        continue

    names = []
    for layout in layouts:
        info = xkb.get_layout_info(layout)
        names.append(info.display_name)

    region = tz.region_from_country_code(country_code)
    if region not in all_country_codes_by_region:
        all_country_codes_by_region[region] = []

    all_country_codes.append(country_code)
    all_country_codes_by_region[region].append(country_code)
    all_keyboard_layouts_by_country_code[country_code] = layouts
    all_keyboard_layout_names_by_country_code[country_code] = names

    for layout in layouts:
        if layout not in all_keyboard_layouts:
            all_keyboard_layouts.append(layout)

for country_code in all_country_codes:
    region = tz.region_from_country_code(country_code)
    if region not in all_regions:
        all_regions.append(region)

all_regions.sort()
for region in all_regions:
    index_in_tz = tz.all_regions.index(region)
    region_name = tz.all_region_names[index_in_tz]
    all_region_names.append(region_name)

all_keyboard_layouts.sort(key=len)
for keyboard_layout in all_keyboard_layouts:
    info = xkb.get_layout_info(keyboard_layout)
    all_keyboard_layout_names.append(info.display_name)

class KeyboardsDataSource():
    def get_all_regions(self) -> list[str]:
        return all_regions

    def find_name_for_region(self, region: str) -> str:
        index = all_regions.index(region)
        return all_region_names[index]

    def get_all_country_codes(self) -> list[str]:
        return all_country_codes

    def get_all_country_codes_by_region(self, region: str) -> list[str]:
        return all_country_codes_by_region[region]

    def find_name_for_country_code(self, country_code: str) -> str:
        return tz.all_country_names_by_code[country_code]

    def get_specials_by_country_code(self, country_code: str) -> list[str]:
        return all_keyboard_layouts_by_country_code[country_code]

    def country_code_from_special(self, special: str) -> str:
        return country_code_from_keyboard(special)

    def region_from_special(self, special: str) -> str:
        return region_from_keyboard(special)

    def search_specials(self, search_term: str, max_results: int) -> tuple[list[str], bool]:
        timezones_filtered, shortened = search_keyboards(search_term, max_results)
        
        return timezones_filtered, shortened

    def find_name_for_special(self, special: str) -> str|None:
        return find_keyboard_layout_name_for_keyboard(special)

    def find_description_for_special(self, special: str) -> str|None:
        return special
