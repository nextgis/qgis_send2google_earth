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

import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, List, Optional

from qgis.PyQt.QtCore import QCoreApplication

from send2google_earth.kml_generator import KmlGenerator


class GoogleEarthRunner(ABC):
    """Abstract base class for launching Google Earth."""

    @abstractmethod
    def run(self, lon: float, lat: float) -> None:
        """
        Run Google Earth with given coordinates.

        :param lon: Longitude.
        :param lat: Latitude.
        """
        raise NotImplementedError

    @staticmethod
    def tr(message: str) -> str:
        """
        Translate the given message.

        :param message: Message to translate.
        :return: Translated string.
        """
        return QCoreApplication.translate(__class__.__name__, message)


class WindowsGoogleEarthRunner(GoogleEarthRunner):
    """Windows implementation of Google Earth runner."""

    _candidate_paths: ClassVar[List[Path]] = [
        Path("C:/Program Files/Google/Google Earth/client/googleearth.exe"),
        Path(
            "C:/Program Files (x86)/Google/Google Earth/client/googleearth.exe"
        ),
        Path(
            "C:/Program Files/Google/Google Earth Pro/client/googleearth.exe"
        ),
        Path(
            "C:/Program Files (x86)/Google/Google Earth Pro/client/googleearth.exe"
        ),
    ]

    def run(self, lon: float, lat: float) -> None:
        """
        Run GE either by association or hardcoded paths.

        :param lon: Longitude.
        :param lat: Latitude.
        """
        kml_file = KmlGenerator.create(lon, lat)
        for candidate in self._candidate_paths:
            if candidate.exists():
                subprocess.Popen([str(candidate), str(kml_file)])
                return

        associated_path = self._get_kml_association()
        if (
            associated_path
            and "googleearth.exe" in associated_path.name.lower()
        ):
            subprocess.Popen([str(associated_path), str(kml_file)])
            return

        raise FileNotFoundError(
            self.tr(
                "Google Earth not found or not associated with .kml files."
            )
        )

    def _get_kml_association(self) -> Optional[Path]:
        """
        Return path to application associated with .kml files.
        Returns None if association not found.
        """
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.kml\UserChoice",
            ) as key:
                prog_id, _ = winreg.QueryValueEx(key, "ProgId")
        except FileNotFoundError:
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ".kml") as key:
                    prog_id, _ = winreg.QueryValueEx(key, "")
            except FileNotFoundError:
                return None

        try:
            with winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command"
            ) as key:
                command, _ = winreg.QueryValueEx(key, "")
                exe_path = Path(command.split('"')[1])
                return exe_path
        except Exception:
            return None


class LinuxGoogleEarthRunner(GoogleEarthRunner):
    """Linux implementation of Google Earth runner."""

    def run(self, lon: float, lat: float) -> None:
        """
        Send coordinates to running Google Earth via xdotool.

        :param lon: Longitude
        :param lat: Latitude
        """
        tool = shutil.which("xdotool")
        if not tool:
            raise RuntimeError(
                self.tr("xdotool not found. Please install it and try again.")
            )

        google_earth_window_name = "Google Earth"

        args = [tool, "search", "--name", google_earth_window_name]
        args.extend(["windowactivate", "--sync", "%@"])
        args.extend(["mousemove", "--window", "%@", "15", "65"])
        args.extend(["click", "--repeat", "3", "1"])

        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                self.tr(
                    "Google Earth is not running. Please start it and try again."
                )
            ) from err

        coordinates_str = f"{lat} {lon}"
        args = [tool, "search", "--name", google_earth_window_name]
        args.extend(["windowactivate", "--sync", "%@"])

        coordinates_keys = ["key", "--window", "%@"]
        for symbol in coordinates_str:
            if symbol == "-":
                symbol = "minus"
            elif symbol == " ":
                symbol = "space"
            elif symbol == ".":
                symbol = "U002E"
            else:
                coordinates_keys.append(symbol)
                continue
            coordinates_keys.append(symbol)

        coordinates_keys.append("Return")
        args.extend(coordinates_keys)

        subprocess.check_call(args)


class MacOSGoogleEarthRunner(GoogleEarthRunner):
    """macOS implementation of Google Earth runner."""

    def run(self, lon: float, lat: float) -> None:
        """
        Run GE via 'open'.

        :param lon: Longitude.
        :param lat: Latitude.
        """
        kml_file = KmlGenerator.create(lon, lat)
        subprocess.Popen(["open", str(kml_file)])
