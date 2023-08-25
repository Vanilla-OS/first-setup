# network.py
#
# Copyright 2023 mirkobrombin
# Copyright 2023 matbme
#
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
from gettext import gettext as _
from threading import Timer

from gi.repository import NM, Adw, Gtk

from vanilla_first_setup.utils.run_async import RunAsync


# Dictionary mapping security types to a tuple containing
# their pretty name and whether it is a secure protocol.
# If security is None, it means that no padlock icon is shown.
# If security is False, a warning symbol appears instead of a padlock.
AP_SECURITY_TYPES = {
    "none": (None, None),
    "wep": (False, _("Insecure network (WEP)")),
    "wpa": (True, _("Secure network (WPA)")),
    "wpa2": (True, _("Secure network (WPA2)")),
    "sae": (True, _("Secure network (WPA3)")),
    "owe": (None, None),
    "owe_tm": (None, None),
}

# PyGObject-libnm doesn't seem to expose these values, so we have redefine them
NM_802_11_AP_FLAGS_PRIVACY = 0x00000001
NM_802_11_AP_SEC_NONE = 0x00000000
NM_802_11_AP_SEC_KEY_MGMT_SAE = 0x00000400
NM_802_11_AP_SEC_KEY_MGMT_OWE = 0x00000800
NM_802_11_AP_SEC_KEY_MGMT_OWE_TM = 0x00001000


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/wireless-row.ui")
class WirelessRow(Adw.ActionRow):
    __gtype_name__ = "WirelessRow"

    signal_icon = Gtk.Template.Child()
    secure_icon = Gtk.Template.Child()
    connected_label = Gtk.Template.Child()

    def __init__(self, ap: NM.AccessPoint, **kwargs):
        super().__init__(**kwargs)
        self.ap = ap
        self.refresh_ui()

    @property
    def ssid(self):
        ssid = self.ap.get_ssid()
        if ssid is not None:
            ssid = ssid.get_data().decode("utf-8")
        else:
            ssid = ""
        return ssid

    def refresh_ui(self):
        # We use the same strength logic as gnome-control-center
        strength = self.ap.get_strength()
        if strength < 20:
            icon_name = "network-wireless-signal-none-symbolic"
        elif strength < 40:
            icon_name = "network-wireless-signal-weak-symbolic"
        elif strength < 50:
            icon_name = "network-wireless-signal-ok-symbolic"
        elif strength < 80:
            icon_name = "network-wireless-signal-good-symbolic"
        else:
            icon_name = "network-wireless-signal-excellent-symbolic"

        self.set_title(self.ssid)
        self.signal_icon.set_from_icon_name(icon_name)
        secure, tooltip = self.__get_security()
        if secure is not None:
            if not secure:
                self.secure_icon.set_from_icon_name("warning-small-symbolic")
            else:
                self.secure_icon.set_from_icon_name("network-wireless-encrypted-symbolic")

        self.secure_icon.set_visible(secure is not None)
        if tooltip is not None:
            self.secure_icon.set_tooltip_text(tooltip)

    def __get_security(self) -> tuple[bool | None, str | None]:
        flags = self.ap.get_flags()
        rsn_flags = self.ap.get_rsn_flags()
        wpa_flags = self.ap.get_wpa_flags()

        # Copying logic used in gnome-control-center because this is a mess
        if (
            not (flags & NM_802_11_AP_FLAGS_PRIVACY)
            and wpa_flags == NM_802_11_AP_SEC_NONE
            and rsn_flags == NM_802_11_AP_SEC_NONE
        ):
            return AP_SECURITY_TYPES["none"]
        elif (
            (flags & NM_802_11_AP_FLAGS_PRIVACY)
            and wpa_flags == NM_802_11_AP_SEC_NONE
            and rsn_flags == NM_802_11_AP_SEC_NONE
        ):
            return AP_SECURITY_TYPES["wep"]
        elif (
            (flags & NM_802_11_AP_FLAGS_PRIVACY)
            and wpa_flags != NM_802_11_AP_SEC_NONE
            and rsn_flags != NM_802_11_AP_SEC_NONE
        ):
            return AP_SECURITY_TYPES["wpa"]
        elif rsn_flags & NM_802_11_AP_SEC_KEY_MGMT_SAE:
            return AP_SECURITY_TYPES["sae"]
        elif rsn_flags & NM_802_11_AP_SEC_KEY_MGMT_OWE:
            return AP_SECURITY_TYPES["owe"]
        elif rsn_flags & NM_802_11_AP_SEC_KEY_MGMT_OWE_TM:
            return AP_SECURITY_TYPES["owe_tm"]
        else:
            return AP_SECURITY_TYPES["wpa2"]


@Gtk.Template(resource_path="/org/vanillaos/FirstSetup/gtk/default-network.ui")
class VanillaDefaultNetwork(Adw.Bin):
    __gtype_name__ = "VanillaDefaultNetwork"

    wired_group = Gtk.Template.Child()
    wireless_group = Gtk.Template.Child()
    hidden_network_row = Gtk.Template.Child()
    proxy_settings_row = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        self.__nm_client = NM.Client.new()

        self.__devices = []
        self.__wired_children = []
        self.__wireless_children = {}

        self.__last_wifi_scan = 0

        # Since we have a dedicated page for checking connectivity,
        # we only need to make sure the user has some type of
        # connection set up, be it wired or wireless.
        self.has_eth_connection = False
        self.has_wifi_connection = False

        self.__get_network_devices()
        self.__start_auto_refresh()

        self.__nm_client.connect("device-added", self.__add_new_device)
        self.__nm_client.connect("device-added", self.__remove_device)
        self.btn_next.connect("clicked", self.__window.next)

    @property
    def step_id(self):
        return self.__key

    def get_finals(self):
        return {}

    def set_btn_next(self, state: bool):
        if state:
            if not self.btn_next.has_css_class("suggested-action"):
                self.btn_next.add_css_class("suggested-action")
            self.btn_next.set_sensitive(True)
        else:
            if self.btn_next.has_css_class("suggested-action"):
                self.btn_next.remove_css_class("suggested-action")
            self.btn_next.set_sensitive(False)

    def __get_network_devices(self):
        devices = self.__nm_client.get_devices()
        eth_devices = 0
        wifi_devices = 0
        for device in devices:
            if device.is_real():
                device_type = device.get_device_type()
                if device_type == NM.DeviceType.ETHERNET:
                    self.__add_ethernet_connection(device)
                    eth_devices += 1
                elif device_type == NM.DeviceType.WIFI:
                    self.__refresh_wifi_list(device)
                    wifi_devices += 1
                else:
                    continue

                self.__devices.append(device)

        self.wired_group.set_visible(eth_devices > 0)
        self.wireless_group.set_visible(wifi_devices > 0)

    def __add_new_device(self, client, device):
        self.__devices.append(device)

    def __remove_device(self, client, device):
        self.__devices.remove(device)

    def __refresh(self):
        for child in self.__wired_children:
            self.wired_group.remove(child)

        self.__wired_children = []

        for device in self.__devices:
            device_type = device.get_device_type()
            if device_type == NM.DeviceType.WIFI:
                self.__scan_wifi(device)

        self.set_btn_next(self.has_eth_connection or self.has_wifi_connection)

    def __start_auto_refresh(self):
        def run_async():
            while True:
                self.__refresh()
                time.sleep(15)

        RunAsync(run_async, None)

    def __device_status(self, conn: NM.Device):
        connected = False
        match conn.get_state():
            case NM.DeviceState.ACTIVATED:
                status = _("Connected")
                connected = True
            case NM.DeviceState.NEED_AUTH:
                status = _("Authentication required")
            case [
                NM.DeviceState.PREPARE,
                NM.DeviceState.CONFIG,
                NM.DeviceState.IP_CONFIG,
                NM.DeviceState.IP_CHECK,
                NM.DeviceState.SECONDARIES,
            ]:
                status = _("Connecting")
            case NM.DeviceState.DISCONNECTED:
                status = _("Disconnected")
            case NM.DeviceState.DEACTIVATING:
                status = _("Disconnecting")
            case NM.DeviceState.FAILED:
                status = _("Connection Failed")
            case NM.DeviceState.UNKNOWN:
                status = _("Status Unknown")
            case NM.DeviceState.UNMANAGED:
                status = _("Unmanaged")
            case NM.DeviceState.UNAVAILABLE:
                status = _("Unavailable")

        return status, connected

    def __add_ethernet_connection(self, conn: NM.DeviceEthernet):
        status, connected = self.__device_status(conn)
        if connected:
            status += f" - {conn.get_speed()} Mbps"
            self.has_eth_connection = True
        else:
            self.has_eth_connection = False

        # Wired devices with no cable plugged in are shown as unavailable
        if conn.get_state() == NM.DeviceState.UNAVAILABLE:
            status = _("Cable Unplugged")

        eth_conn = Adw.ActionRow(title=status)
        self.wired_group.add(eth_conn)
        self.__wired_children.append(eth_conn)

    def __refresh_wifi_list(self, conn: NM.DeviceWifi):
        while conn.get_last_scan() == self.__last_wifi_scan:
            time.sleep(0.25)

        networks = {}
        for ap in conn.get_access_points():
            ssid = ap.get_ssid()
            if ssid is None:
                continue

            ssid = ssid.get_data().decode("utf-8")
            if ssid in networks.keys():
                networks[ssid].append(ap)
            else:
                networks[ssid] = [ap]

        # Invalidate current list
        for ssid, (child, clean) in self.__wireless_children.items():
            self.__wireless_children[ssid] = (child, True)

        for ssid, aps in networks.items():
            max_strength = -1
            best_ap = None
            for ap in aps:
                ap_strength = ap.get_strength()
                if ap_strength > max_strength:
                    max_strength = ap_strength
                    best_ap = ap

            # Try to re-use entries with the same SSID
            if ssid in self.__wireless_children.keys():
                child = self.__wireless_children[ssid][0]
                child.ap = best_ap
                child.refresh_ui()
                self.__wireless_children[ssid] = (child, False)
                continue

            # Create new row if SSID is new
            wifi_network = WirelessRow(best_ap)
            self.wireless_group.add(wifi_network)
            self.__wireless_children[ssid] = (wifi_network, False)

        # Remove invalid rows
        invalid_ssids = []
        for ssid, (child, clean) in self.__wireless_children.items():
            if clean:
                self.wireless_group.remove(child)
                invalid_ssids.append(ssid)

        for ssid in invalid_ssids:
            del self.__wireless_children[ssid]

    def __scan_wifi(self, conn: NM.DeviceWifi):
        self.__last_wifi_scan = conn.get_last_scan()
        conn.request_scan_async()
        print("Running scan")

        t = Timer(1.5, self.__refresh_wifi_list, [conn])
        t.start()
