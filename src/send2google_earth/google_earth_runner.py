# QGIS DevTools Plugin
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

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import shutil
import subprocess


class GoogleEarthRunner(ABC):
    """Abstract base class for launching Google Earth."""

    @abstractmethod
    def run(self, kml_file: Path) -> None:
        """
        Run Google Earth with the given KML file.

        :param kml_file: Path to the KML file.
        """
        raise NotImplementedError


class WindowsGoogleEarthRunner(GoogleEarthRunner):
    """Windows implementation of Google Earth runner."""

    _candidate_paths = [
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

    def run(self, kml_file: Path) -> None:
        """
        Run GE either by association or hardcoded paths.

        :param kml_file: Path to the KML file.
        """
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
            "Google Earth not found or not associated with .kml files."
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

    _candidate_binaries = ["google-earth", "google-earth-pro"]

    def run(self, kml_file: Path) -> None:
        """
        Run GE via binary or flatpak.

        :param kml_file: Path to the KML file.
        """
        for binary in self._candidate_binaries:
            ge_path = shutil.which(binary)
            if ge_path:
                subprocess.Popen([ge_path, str(kml_file)])
                return

        # Try Flatpak
        flatpak_bin = shutil.which("flatpak")
        if flatpak_bin:
            result = subprocess.run(
                [flatpak_bin, "list"], capture_output=True, text=True
            )
            if "com.google.GoogleEarthPro" in result.stdout:
                subprocess.Popen(
                    [
                        flatpak_bin,
                        "run",
                        "com.google.GoogleEarthPro",
                        str(kml_file),
                    ]
                )
                return

        raise FileNotFoundError(
            "Google Earth not found (neither binary nor Flatpak)."
        )


class MacOSGoogleEarthRunner(GoogleEarthRunner):
    """macOS implementation of Google Earth runner."""

    def run(self, kml_file: Path) -> None:
        """
        Run GE via 'open'.

        :param kml_file: Path to the KML file.
        """
        subprocess.Popen(["open", str(kml_file)])
