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

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QAction

from qgis.core import *

from .compat import get_file_dir
from .send2google_earthtool import Send2GEtool


class Send2GE:
  def __init__(self, iface):
    """Initialize class"""
    # save reference to QGIS interface
    self.iface = iface
    self.plugin_dir = get_file_dir(__file__)

  def initGui(self):
    """Initialize graphic user interface"""
    #create action that will be run by the plugin
    self.action = QAction(
        QIcon("%s/icons/cursor2.png" % self.plugin_dir),
        "Send to Google Earth",
        self.iface.mainWindow()
    )
    self.action.setWhatsThis("Send to Google Earth")
    self.action.setStatusTip("Send coordinates of a mouse click to Google Earth")
    
    # add plugin menu to Vector toolbar
    self.iface.addPluginToMenu("Send2GoogleEarth",self.action)
    
    # add icon to new menu item in Vector toolbar
    self.iface.addToolBarIcon(self.action)

    # connect action to the run method
    self.action.triggered.connect(self.run)

    # prepare map tool
    self.mapTool = Send2GEtool(self.iface)
    #self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)
      
  def unload(self):
    """Actions to run when the plugin is unloaded"""
    # remove menu and icon from the menu
    self.iface.removeToolBarIcon(self.action)
    self.iface.removePluginMenu("Send2GoogleEarth",self.action)

    if self.iface.mapCanvas().mapTool() == self.mapTool:
      self.iface.mapCanvas().unsetMapTool(self.mapTool)

    del self.mapTool

  def run(self):
    """Action to run"""
    # create a string and show it

    self.iface.mapCanvas().setMapTool(self.mapTool)
