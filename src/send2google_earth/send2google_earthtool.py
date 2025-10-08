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

from pathlib import Path

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
)
from qgis.gui import QgisInterface, QgsMapTool
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QCursor, QMouseEvent, QPixmap
from qgis.PyQt.QtWidgets import QApplication, QMessageBox

from send2google_earth.google_earth_runner_factory import (
    GoogleEarthRunnerFactory,
)


class Send2GEtool(QgsMapTool):
    """
    Map tool to capture mouse clicks and send coordinates to Google Earth.
    """

    def __init__(self, iface: QgisInterface) -> None:
        """Initialize the map tool.

        :param iface: An interface instance provided by QGIS.
        :type iface: QgisInterface
        """
        super().__init__(iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        self.iface = iface

        self.plugin_dir = Path(__file__).parent

        self.cursor = QCursor(
            QPixmap(str(self.plugin_dir / "icons" / "cursor2.png")), 1, 1
        )

    def activate(self) -> None:
        self.canvas.setCursor(self.cursor)

    def canvasReleaseEvent(self, event: QMouseEvent) -> None:
        """Handle mouse release event on the canvas.

        :param event: Mouse release event from QGIS canvas.
        :type event: QMouseEvent
        """
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        coord_x = event.pos().x()
        coord_y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(
            coord_x, coord_y
        )
        QApplication.restoreOverrideCursor()

        crs_src = self.canvas.mapSettings().destinationCrs()
        crs_wgs = QgsCoordinateReferenceSystem("EPSG:4326")

        if crs_src.authid() != "4326":
            xform = QgsCoordinateTransform(
                crs_src, crs_wgs, self.canvas.mapSettings().transformContext()
            )
            point = xform.transform(point)

        try:
            runner = GoogleEarthRunnerFactory.create()
            runner.run(point.x(), point.y())
        except Exception as err:
            QMessageBox.warning(
                self.canvas,
                self.tr("Error"),
                self.tr("Failed to run Google Earth: {}").format(err),
            )
