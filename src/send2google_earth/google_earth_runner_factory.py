# Send2GE Plugin
# Copyright (C) 2025  NextGIS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.

import platform

from qgis.PyQt.QtCore import QCoreApplication

from send2google_earth.google_earth_runner import (
    GoogleEarthRunner,
    LinuxGoogleEarthRunner,
    MacOSGoogleEarthRunner,
    WindowsGoogleEarthRunner,
)


class GoogleEarthRunnerFactory:
    """Factory to create platform-specific Google Earth runner."""

    @staticmethod
    def create() -> GoogleEarthRunner:
        """
        Return platform-specific runner.
        """
        system = platform.system()
        if system == "Windows":
            return WindowsGoogleEarthRunner()
        if system == "Linux":
            return LinuxGoogleEarthRunner()
        if system == "Darwin":
            return MacOSGoogleEarthRunner()
        raise NotImplementedError(
            QCoreApplication.translate(
                "GoogleEarthRunnerFactory", "Unsupported OS: {}"
            ).format(system)
        )
