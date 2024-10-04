# -*- coding: utf-8 -*-
# ******************************************************************************
#
# Send2Google_Earth
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and sends them to Google Earth
#
# Copyright (C) 2013-2015 Maxim Dubinin (sim@gis-lab.info), NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
# ******************************************************************************

import os
import tempfile
import platform
import subprocess

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication, QMessageBox

from qgis.core import *
from qgis.gui import *

from .compat import get_file_dir, PY3
from .qgis23 import QgsCoordinateTransform


class Send2GEtool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        # self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface

        self.plugin_dir = get_file_dir(__file__)

        self.cursor = QCursor(
            QPixmap("%s/icons/cursor2.png" % self.plugin_dir), 1, 1
        )

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def create_kml(x, y):
        return f

    def canvasReleaseEvent(self, event):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        QApplication.restoreOverrideCursor()

        crsSrc = self.canvas.mapSettings().destinationCrs()
        crsWGS = QgsCoordinateReferenceSystem(4326)

        if crsSrc.authid() != "4326":
            xform = QgsCoordinateTransform(crsSrc, crsWGS)
            point = xform.transform(point)

        if PY3:
            f = tempfile.NamedTemporaryFile(
                suffix=".kml", delete=False, mode="w", encoding="utf-8"
            )
        else:
            f = tempfile.NamedTemporaryFile(
                suffix=".kml", delete=False, mode="w"
            )
        f.write(r'<?xml version="1.0" encoding="UTF-8"?>')
        f.write(
            r'<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
        )
        f.write(r"<Document>")
        f.write(r"   <name>" + f.name + r"</name>")
        f.write(r"   <Placemark>")
        f.write(r"       <Point>")
        f.write(r"       <name>test</name>")
        f.write(
            r"           <coordinates>"
            + str(point.x())
            + ","
            + str(point.y())
            + r",0</coordinates>"
        )
        f.write(r"       </Point>")
        f.write(r"   </Placemark>")
        f.write(r"</Document>")
        f.write(r"</kml>")
        f.close()

        linpath = "google-earth"

        unknown = False
        ret = 0

        if platform.system() == "Windows":
            winpath = (
                r"C:/Program Files/Google/Google Earth/client/googleearth.exe"
            )
            if not os.path.exists(winpath):
                winpath = r"C:/Program Files (x86)/Google/Google Earth/client/googleearth.exe"
            if not os.path.exists(winpath):
                winpath = r"C:/Program Files (x86)/Google/Google Earth Pro/client/googleearth.exe"
            if not os.path.exists(winpath):
                winpath = r"C:/Program Files/Google/Google Earth Pro/client/googleearth.exe"

            if event.modifiers() == Qt.ShiftModifier:
                subprocess.Popen([winpath, f.name])
            else:
                os.startfile(f.name)

        elif platform.system() == "Linux":
            google_earth_window_name = "Google Earth"
            tool = "xdotool"
            args = [tool, "search", "--name", google_earth_window_name]
            args.extend(["windowactivate", "--sync", "%@"])
            args.extend(["mousemove", "--window", "%@", "15", "65"])
            args.extend(["click", "--repeat", "3", "1"])
            try:
                subprocess.check_call(args)
            except OSError as err:
                QMessageBox.warning(
                    self.canvas,
                    "Error",
                    "There is no xdotool util in system. Please install it and try again.",
                )
                return
            except subprocess.CalledProcessError as err:
                QMessageBox.warning(
                    self.canvas,
                    "Error",
                    "There is no Google Earth running. Please run it and try again.",
                )
                return

            args = [tool, "search", "--name", google_earth_window_name]
            args.extend(["windowactivate", "--sync", "%@"])
            coordinates_str = "%s %s" % (
                point.y(),
                point.x(),
            )
            coordinates_keys = [
                "key",
                "--window",
                "%@",
            ]
            for symbol in coordinates_str:
                if symbol == "-":
                    symbol = "minus"
                elif symbol == " ":
                    symbol = "space"
                elif symbol == ".":
                    symbol = "U002E"
                coordinates_keys.append(symbol)
            args.extend(coordinates_keys)
            args.extend(["Return"])
            subprocess.call(args)

        elif platform.system() == "Darwin":
            ret = os.system("open " + f.name)
        else:
            unknown = True

        if unknown is True:
            QMessageBox.warning(
                self.canvas,
                "Error",
                "Unknown operation system. Please let developers of the plugin know.",
            )
        if ret != 0:
            QMessageBox.warning(
                self.canvas,
                "Error",
                "Unable to send to GE, executable not found.\n I tried "
                + linpath,
            )

        # os.unlink(f.name)
