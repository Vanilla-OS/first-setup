import os

import vanilla_first_setup.core.timezones as tz

all_regions = []
all_country_codes = []
all_locales = []
country_codes_by_region = {}
locales_by_country_code = {}
locale_name_by_locale = {}

with open('/usr/share/i18n/SUPPORTED', 'r') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.split(" ")
        if len(parts) < 2 or "UTF-8" not in parts[1]:
            continue
        loc = parts[0]
        lang_with_country = loc.split(".")[0].split("_")
        lang = lang_with_country[0]
        if len(lang_with_country) < 2:
            continue
        country_code = lang_with_country[1].split("@")[0]
        if country_code not in tz.all_country_codes:
            continue

        region = tz.region_from_country_code(country_code)
        if region not in all_regions:
            all_regions.append(region)
            country_codes_by_region[region] = []
        if country_code not in country_codes_by_region[region]:
            country_codes_by_region[region].append(country_code)

        if country_code not in all_country_codes:
            all_country_codes.append(country_code)
            locales_by_country_code[country_code] = []
        if loc not in locales_by_country_code[country_code]:
            locales_by_country_code[country_code].append(loc)
        
        all_locales.append(loc)

def country_code_from_locale(loc):
    for country_code, loc_list in locales_by_country_code.items():
        if loc in loc_list:
            return country_code
    return ""

def region_from_locale(loc):
    country_code = country_code_from_locale(loc)
    for region, country_code_list in country_codes_by_region.items():
        if country_code in country_code_list:
            return region
    return ""

for loc in all_locales:
    loc_first_part = loc.split(".")[0]
    filename = os.path.join('/usr/share/i18n/locales/', loc_first_part)
    if not os.path.isfile(filename):
        locale_name_by_locale[loc] = loc
        continue
    lang_name = ""
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("lang_name"):
                split_line = line.split()
                if len(split_line) >= 2:
                    lang_name = split_line[1].replace("\"", "").replace("\n", "")
    if lang_name == "":
        lang_name = loc
    locale_name_by_locale[loc] = lang_name + " (" + tz.all_country_names_by_code[country_code_from_locale(loc)] + ")"


def search_locales(search_term: str, limit: int) -> tuple[list[str], bool]:
    clean_search_term = search_term.lower()

    locales_filtered = []
    list_shortened = False
    for loc in all_locales:
        locale_name = locale_name_by_locale[loc]
        if len(locales_filtered) >= limit:
            list_shortened = True
            break
        does_match = True
        for search_term_part in clean_search_term.split():
            if search_term_part not in locale_name.lower():
                does_match = False
        if does_match:
            locales_filtered.append(loc)
    return (locales_filtered, list_shortened)

class LanguagesDataSource():
    def get_all_regions(self) -> list[str]:
        return all_regions

    def find_name_for_region(self, region: str) -> str:
        index = tz.all_regions.index(region)
        return tz.all_region_names[index]

    def get_all_country_codes(self) -> list[str]:
        return all_country_codes

    def get_all_country_codes_by_region(self, region: str) -> list[str]:
        return country_codes_by_region[region]

    def find_name_for_country_code(self, country_code: str) -> str:
        return tz.all_country_names_by_code[country_code]

    def get_specials_by_country_code(self, country_code: str) -> list[str]:
        return locales_by_country_code[country_code]

    def country_code_from_special(self, special: str) -> str:
        return country_code_from_locale(special)

    def region_from_special(self, special: str) -> str:
        return region_from_locale(special)

    def search_specials(self, search_term: str, max_results: int) -> tuple[list[str], bool]:
        locales_filtered, shortened = search_locales(search_term, max_results)
        
        return locales_filtered, shortened

    def find_name_for_special(self, special: str) -> str|None:
        return locale_name_by_locale[special]

    def find_description_for_special(self, special: str) -> str|None:
        return special