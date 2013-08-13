# -*- coding: utf-8 -*-
#******************************************************************************
#
# Send2Google_Earth
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and sends them to Google Earth
#
# Copyright (C) 2013 Maxim Dubinin (sim@gis-lab.inf), NextGIS (info@nextgis.org)
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
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import resources
import os
import tempfile

class Send2GEtool(QgsMapTool):
  def __init__(self, iface):
    QgsMapTool.__init__(self, iface.mapCanvas())

    self.canvas = iface.mapCanvas()
    #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
    self.iface = iface

    self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)

  def activate(self):
    self.canvas.setCursor(self.cursor)

  def canvasReleaseEvent(self, event):

    QApplication.setOverrideCursor(Qt.WaitCursor)
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    QApplication.restoreOverrideCursor()

    f = tempfile.NamedTemporaryFile(suffix = ".kml",delete=False)
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">')
    f.write('<Document>')
    f.write('   <name>' + f.name + '</name>')
    f.write('   <Placemark>')
    f.write('       <Point>')
    f.write('       <name>test</name>')
    f.write('           <coordinates>' + str(point.x()) +','+ str(point.y()) + ',0</coordinates>')
    f.write('       </Point>')
    f.write('   </Placemark>')
    f.write('</Document>')
    f.write('</kml>')
    f.close()

    winpath = "c:/Program Files/Google/googleearth.exe"
    if os.path.exists(winpath):
      ret = os.system("\"" + winpath + "\""+ f.name)
    else:
      ret = os.system("google-earth " + f.name)

    if ret != 0:
      QMessageBox.warning(self.canvas,"Error","Unable to send to GE, executable not found"
                         )
    os.unlink(f.name)
