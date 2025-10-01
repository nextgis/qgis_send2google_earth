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
from pathlib import Path
import platform
import subprocess

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication, QMessageBox

from qgis.core import *
from qgis.gui import *

from send2google_earth.google_earth_runner_factory import (
    GoogleEarthRunnerFactory,
)


class Send2GEtool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        # self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface

        self.plugin_dir = Path(__file__).parent

        self.cursor = QCursor(
            QPixmap(str(self.plugin_dir / "icons" / "cursor2.png")), 1, 1
        )

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def canvasReleaseEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        QApplication.restoreOverrideCursor()

        crsSrc = self.canvas.mapSettings().destinationCrs()
        crsWGS = QgsCoordinateReferenceSystem("EPSG:4326")

        if crsSrc.authid() != "4326":
            xform = QgsCoordinateTransform(
                crsSrc, crsWGS, self.canvas.mapSettings().transformContext()
            )
            point = xform.transform(point)

        try:
            runner = GoogleEarthRunnerFactory.create()
            runner.run(point.x(), point.y())
        except Exception as err:
            QMessageBox.warning(
                self.canvas,
                "Error",
                f"Failed to run Google Earth: {err}",
            )
