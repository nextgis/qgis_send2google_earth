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

from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from send2google_earth.about_dialog import AboutDialog
from send2google_earth.send2google_earthtool import Send2GEtool


class Send2GE:
    """QGIS Plugin to send map coordinates to Google Earth."""

    def __init__(self, iface: QgisInterface) -> None:
        """
        Initialize class

        :param iface: An interface instance provided by QGIS.
        :type iface: QgisInterface
        """
        self.iface = iface
        self.plugin_dir = Path(__file__).parent
        self._translator = None
        self.__init_translator()

        self.map_tool = Send2GEtool(self.iface)

    def __init_translator(self) -> None:
        """Initialize translation support."""
        locale = QgsApplication.instance().locale()
        locale_file = (
            self.plugin_dir / "i18n" / f"send2google_earth_{locale}.qm"
        )

        if not locale_file.exists():
            return

        translator = QTranslator()
        translator.load(str(locale_file))
        QCoreApplication.installTranslator(translator)
        self._translator = translator

    def initGui(self) -> None:
        """Create actions and add them to the QGIS GUI."""
        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("Send2GoogleEarth")
        self.menu.setIcon(QIcon(str(self.plugin_dir / "icons" / "icon.png")))

        self.send_click_action = QAction(
            QIcon(str(self.plugin_dir / "icons" / "cursor2.png")),
            self.tr("Send to Google Earth"),
            self.iface.mainWindow(),
        )
        self.send_click_action.setWhatsThis(self.tr("Send to Google Earth"))
        self.send_click_action.setStatusTip(
            self.tr("Send coordinates of a mouse click to Google Earth")
        )
        self.send_click_action.triggered.connect(self.run)

        self.action_about = QAction(
            QgsApplication.getThemeIcon("mActionPropertiesWidget.svg"),
            self.tr("About plugin…"),
            self.iface.mainWindow(),
        )
        self.action_about.triggered.connect(self.about)

        self.menu.addAction(self.send_click_action)
        self.menu.addAction(self.action_about)

        self.iface.pluginMenu().addMenu(self.menu)

        self.iface.addToolBarIcon(self.send_click_action)

        self.__show_help_action = QAction(
            QIcon(str(self.plugin_dir / "icons" / "icon.png")),
            "Send2GE",
        )
        self.__show_help_action.triggered.connect(self.about)
        plugin_help_menu = self.iface.pluginHelpMenu()
        assert plugin_help_menu is not None
        plugin_help_menu.addAction(self.__show_help_action)

    def unload(self) -> None:
        """Remove actions and toolbar icon when the plugin is unloaded."""
        self.iface.removeToolBarIcon(self.send_click_action)

        if self.menu is not None:
            self.iface.pluginMenu().removeAction(self.menu.menuAction())
            self.menu.deleteLater()

        self.send_click_action.deleteLater()
        self.action_about.deleteLater()

        plugin_help_menu = self.iface.pluginHelpMenu()
        assert plugin_help_menu is not None
        plugin_help_menu.removeAction(self.__show_help_action)
        self.__show_help_action.deleteLater()

        if self.iface.mapCanvas().mapTool() == self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)

        del self.map_tool

    def run(self) -> None:
        """Set the map tool for capturing clicks."""
        self.iface.mapCanvas().setMapTool(self.map_tool)

    def tr(self, message: str) -> str:
        """
        Translate the given message.

        :param message: Message to be translated.
        :type message: str

        :return: Translated message string.
        :rtype: str
        """
        return QCoreApplication.translate(__class__.__name__, message)

    def about(self) -> None:
        """Show the About dialog."""
        dialog = AboutDialog(self.plugin_dir.name)
        dialog.exec()
