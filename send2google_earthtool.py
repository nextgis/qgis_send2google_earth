# -*- coding: utf-8 -*-
#******************************************************************************
#
# Send2Google_Earth
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and sends them to Google Earth
#
# Copyright (C) 2013 Maxim Dubinin (sim@gis-lab.info), NextGIS (info@nextgis.org)
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
import platform

class Send2GEtool(QgsMapTool):
  def __init__(self, iface):
    QgsMapTool.__init__(self, iface.mapCanvas())

    self.canvas = iface.mapCanvas()
    #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
    self.iface = iface

    self.cursor = QCursor(QPixmap(":/icons/cursor2.png"), 1, 1)

  def activate(self):
    self.canvas.setCursor(self.cursor)

  def create_kml(x,y):
    
    
    return f
  
  def canvasReleaseEvent(self, event):

    QApplication.setOverrideCursor(Qt.WaitCursor)
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    QApplication.restoreOverrideCursor()

    crsSrc = self.canvas.mapRenderer().destinationCrs()
    crsWGS = QgsCoordinateReferenceSystem(4326)
    
    if crsSrc.authid() != "4326":
        xform = QgsCoordinateTransform(crsSrc, crsWGS)
        point = xform.transform(QgsPoint(point.x(),point.y()))
    
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

    winpath = "C:/Program Files/Google/Google Earth/client/googleearth.exe"
    linpath = "google-earth"
    unknown = False
    ret = 0
    
    if platform.system() == 'Windows':
      #cmd = "start /B " + "\"" + winpath + "\" "+ f.name
      #ret = os.system(cmd)
      os.startfile(f.name)
    elif platform.system() == 'Linux':
      ret = os.system(linpath + " " + f.name)
    elif platform.system() == "Darwin":
      ret = os.system("open " + f.name)
    else:
      unknown = True

    if unknown == True:
      QMessageBox.warning(self.canvas,"Error","Unknown operation system. Please let developers of the plugin know.")
    if ret != 0:
      QMessageBox.warning(self.canvas,"Error","Unable to send to GE, executable not found.\n I tried " + linpath)
    
    #os.unlink(f.name)
