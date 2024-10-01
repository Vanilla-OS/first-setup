# network.py
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
from collections import OrderedDict
from requests import Session

logger = logging.getLogger("FirstSetup::Connector")


def check_connection():
    try:
        s = Session()
        headers = OrderedDict(
            {
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "vanillaos.org",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            }
        )
        s.headers = headers
        s.get("https://vanillaos.org/", headers=headers, verify=True)
        return True
    except Exception as e:
        logger.error(f"Connection check failed: {str(e)}")
        return False
