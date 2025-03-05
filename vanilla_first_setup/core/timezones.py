import gi

gi.require_version("GWeather", "4.0")

from datetime import datetime
import logging
import threading
import copy
_ = __builtins__["_"]

import requests
from gi.repository import GLib, GWeather
import pytz

logger = logging.getLogger("FirstSetup::Timezones")

world = GWeather.Location.get_world()
base = world

all_country_codes: list[str] = []
all_regions: list[str] = []
all_region_names: list[str] = []
all_country_codes_by_region: dict[str, list[str]] = {}
all_timezones_by_country_code: dict[str, list[str]] = {}
all_country_names_by_code: dict[str, str] = {}
user_location: GWeather.Location|None = None
user_country: str|None = None
user_country_code: str|None = None
user_city: str|None = None
user_timezone: str|None = None
user_region: str|None = None

def register_location_callback(callback):
    if user_location:
        callback(user_location)
    __location_callbacks.append(callback)

def get_timezone_preview(tzname):
    timezone = pytz.timezone(tzname)
    now = datetime.now(timezone)
    now_str = (
        "%02d:%02d" % (now.hour, now.minute),
        now.strftime("%A, %d %B %Y"),
    )
    return now_str

def region_from_timezone(tzname):
    return tzname.split("/")[0]

def region_from_country_code(country_code) -> str:
    for region, tz_country_codes in all_country_codes_by_region.items():
        for tz_country_code in tz_country_codes:
            if country_code == tz_country_code:
                return region
    return ""
        
def country_code_from_timezone(timezone) -> str:
    for country_code, tzcc_timezones in all_timezones_by_country_code.items():
        for tzcc_timezone in tzcc_timezones:
            if timezone == tzcc_timezone:
                return country_code
    return ""

def retrieve_country_names_by_region(region) -> list[str]:
    country_codes = all_country_codes_by_region[region]
    countries = copy.deepcopy(country_codes)
    for idx, country_code in enumerate(countries):
        countries[idx] = all_country_names_by_code[country_code]
    return countries

__user_prefers_layout = False
__user_preferred_region: str|None = None
__user_preferred_country_code: str|None = None

def has_user_preferred_location() -> bool:
    return __user_prefers_layout

def get_user_preferred_location() -> tuple[str, str, str]:
    return (__user_preferred_region, __user_preferred_country_code)

def set_user_preferred_location(region, country_code=None):
    if not region:
        return
    global __user_prefers_layout
    global __user_preferred_region
    global __user_preferred_country_code
    global __user_preferred_timezone
    __user_preferred_region = region
    __user_preferred_country_code = country_code
    __user_prefers_layout = True

__region_translations = {'Europe': _('Europe'),
                         'Asia': _('Asia'),
                         'America': _('America'),
                         'Africa': _('Africa'),
                         'Antarctica': _('Antarctica'),
                         'Pacific': _('Pacific Ocean'),
                         'Australia': _('Australia'),
                         'Atlantic': _('Atlantic Ocean'),
                         'Indian': _('Indian Ocean'),
                         'Arctic': _('Arctic'),
                         }
__location_callbacks = []

for country_code in pytz.country_timezones:
    timezones = pytz.country_timezones[country_code]
    country_name = pytz.country_names[country_code]
    region = region_from_timezone(timezones[0])

    all_country_codes.append(country_code)
    
    if region not in all_country_codes_by_region:
        all_country_codes_by_region[region] = []
        all_regions.append(region)
    all_country_codes_by_region[region].append(country_code)

    all_timezones_by_country_code[country_code] = timezones

    all_country_names_by_code[country_code] = country_name

all_regions.sort()
for region in all_regions:
    if region in __region_translations:
        all_region_names.append(__region_translations[region])

def search_timezones_by_country(search_term: str, limit: int) -> tuple[list[str], bool]:
    '''
        search_countries looks for all country names with substring search_term and returns their time zones

        search is not case sensitive
    
        returns a list of all time zones for the countries that have matching names and a bool if the list is shortened due to the limit
    '''
    clean_search_term = search_term.lower()

    timezones_filtered = []
    list_shortened = False

    for country_code, country_name in all_country_names_by_code.items():
        if len(timezones_filtered) > limit:
            list_shortened = True
            break
        if clean_search_term in country_name.lower():
            timezones_filtered += all_timezones_by_country_code[country_code]
    
    return (timezones_filtered, list_shortened)

def search_timezones(search_term: str, limit: int) -> tuple[list[str], bool]:
    '''
        search_timezones looks for all time zones with substring search_term

        search is not case sensitive
    
        returns a list of all matching time zones and a bool if the list is shortened due to the limit
    '''
    clean_search_term = search_term.lower().replace(" ", "_") 

    timezones_filtered = []
    list_shortened = False
    for country_codes, timezones in all_timezones_by_country_code.items():
        if len(timezones_filtered) > limit:
            list_shortened = True
            break
        for timezone in timezones:
            if clean_search_term in timezone.lower():
                timezones_filtered.append(timezone)
    return (timezones_filtered, list_shortened)

def __update_user_location(location):
    global user_location
    global user_country
    global user_country_code
    global user_city
    global user_timezone
    global user_region
    user_location = location
    user_country = location.get_country_name()
    user_city = location.get_city_name()
    user_timezone = location.get_timezone().get_identifier()
    user_region = region_from_timezone(user_timezone)
    if location.get_country() in all_country_codes:
        user_country_code = location.get_country()

    for callback in __location_callbacks:
        GLib.idle_add(callback, location)

def __retrieve_location_thread():
    logger.info("Trying to retrieve timezone automatically")
    try:
        res = requests.get("http://ip-api.com/json?fields=49344", timeout=10).json()
        if res["status"] != "success":
            raise Exception(
                f"get_location: request failed with message '{res['message']}'"
            )
        nearest = world.find_nearest_city(res["lat"], res["lon"])
    except Exception as e:
        logger.error(f"Failed to retrieve user location automatically.")
        nearest = None

    if nearest:
        __update_user_location(nearest)

    logger.info("Done retrieving timezone")

thread = threading.Thread(target=__retrieve_location_thread)
thread.start()

class TimezonesDataSource():
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
        return all_country_names_by_code[country_code]

    def get_specials_by_country_code(self, country_code: str) -> list[str]:
        return all_timezones_by_country_code[country_code]

    def country_code_from_special(self, special: str) -> str:
        return country_code_from_timezone(special)

    def region_from_special(self, special: str) -> str:
        return region_from_timezone(special)

    def search_specials(self, search_term: str, max_results: int) -> tuple[list[str], bool]:
        timezones_filtered, shortened = search_timezones(search_term, max_results)

        if max_results-len(timezones_filtered) > 0:
            timezones_filtered_new, shortened = search_timezones_by_country(search_term, max_results-len(timezones_filtered))
            timezones_filtered += timezones_filtered_new
        
        return timezones_filtered, shortened

    def find_name_for_special(self, special: str) -> str|None:
        return special.split("/")[1]

    def find_description_for_special(self, special: str) -> str|None:
        return get_timezone_preview(special)[0]
