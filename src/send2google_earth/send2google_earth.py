# -*- coding: utf-8 -*-
# ******************************************************************************
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
# ******************************************************************************
import os
from os import path
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QTranslator, QCoreApplication

from qgis.core import *
from qgis.core import QgsApplication

from .compat import get_file_dir
from .send2google_earthtool import Send2GEtool
from . import about_dialog


class Send2GE:
    def __init__(self, iface):
        """Initialize class"""
        # save reference to QGIS interface
        self.iface = iface
        self.plugin_dir = get_file_dir(__file__)
        self._translator = None
        self.__init_translator()

    def __init_translator(self):
        # initialize locale
        locale = QgsApplication.instance().locale()

        def add_translator(locale_path):
            if not path.exists(locale_path):
                return
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            self._translator = translator  # Should be kept in memory

        add_translator(
            path.join(
                self.plugin_dir,
                "i18n",
                "send2google_earth_{}.qm".format(locale),
            )
        )

    def initGui(self):
        """Initialize graphic user interface"""
        # create action that will be run by the plugin
        self.action = QAction(
            QIcon("%s/icons/cursor2.png" % self.plugin_dir),
            "Send to Google Earth",
            self.iface.mainWindow(),
        )
        self.action.setWhatsThis("Send to Google Earth")
        self.action.setStatusTip(
            "Send coordinates of a mouse click to Google Earth"
        )

        self.actionAbout = QAction(self.tr("About"), self.iface.mainWindow())

        # add plugin menu to Vector toolbar
        self.iface.addPluginToMenu("Send2GoogleEarth", self.action)
        self.iface.addPluginToMenu("Send2GoogleEarth", self.actionAbout)

        # add icon to new menu item in Vector toolbar
        self.iface.addToolBarIcon(self.action)

        # connect action to the run method
        self.action.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

        # prepare map tool
        self.mapTool = Send2GEtool(self.iface)
        # self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

    def unload(self):
        """Actions to run when the plugin is unloaded"""
        # remove menu and icon from the menu
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("Send2GoogleEarth", self.action)
        self.iface.removePluginMenu("Send2GoogleEarth", self.actionAbout)
        self.action.deleteLater()
        self.actionAbout.deleteLater()

        if self.iface.mapCanvas().mapTool() == self.mapTool:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)

        del self.mapTool

    def run(self):
        """Action to run"""
        # create a string and show it

        self.iface.mapCanvas().setMapTool(self.mapTool)

    def tr(self, message):
        return QCoreApplication.translate(__class__.__name__, message)

    def about(self):
        dialog = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec_()
