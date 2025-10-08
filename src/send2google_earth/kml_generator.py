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

import tempfile
from pathlib import Path


class KmlGenerator:
    """Generator class for temporary KML files."""

    @classmethod
    def create(cls, lon: float, lat: float) -> Path:
        """
        Create temporary KML file with given coordinates.

        :param lon: Longitude.
        :param lat: Latitude.

        :return: Path to created KML file.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".kml", delete=False, mode="w", encoding="utf-8"
        ) as kml_file:
            kml_file.write('<?xml version="1.0" encoding="UTF-8"?>')
            kml_file.write(
                '<kml xmlns="http://www.opengis.net/kml/2.2" '
                'xmlns:gx="http://www.google.com/kml/ext/2.2" '
                'xmlns:kml="http://www.opengis.net/kml/2.2" '
                'xmlns:atom="http://www.w3.org/2005/Atom">'
            )
            kml_file.write("<Document>")
            kml_file.write(f"<name>{Path(kml_file.name).name}</name>")
            kml_file.write("<Placemark>")
            kml_file.write("<Point>")
            kml_file.write("<name>QGIS Point</name>")
            kml_file.write(f"<coordinates>{lon},{lat},0</coordinates>")
            kml_file.write("</Point>")
            kml_file.write("</Placemark>")
            kml_file.write("</Document>")
            kml_file.write("</kml>")
            return Path(kml_file.name)
