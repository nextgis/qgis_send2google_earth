# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Send2Google_Earth
                                 A QGIS plugin
 Collection of internet map services
                              -------------------
        begin                : 2014-11-21
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


import os
import sys
from qgis.PyQt.QtCore import QT_VERSION_STR, Qt

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Qt compatibility layer for PyQt5/PyQt6 support
QT_MAJOR_VERSION = int(QT_VERSION_STR.split('.')[0])


def exec_dialog(dialog):
    """Execute dialog with proper method for Qt5/Qt6 compatibility"""
    if QT_MAJOR_VERSION >= 6:
        return dialog.exec()
    else:
        return dialog.exec_()


def get_wait_cursor():
    """Get wait cursor constant for Qt5/Qt6 compatibility"""
    if QT_MAJOR_VERSION >= 6:
        return Qt.CursorShape.WaitCursor
    else:
        return Qt.WaitCursor


def get_shift_modifier():
    """Get Shift modifier constant for Qt5/Qt6 compatibility"""
    if QT_MAJOR_VERSION >= 6:
        return Qt.KeyboardModifier.ShiftModifier
    else:
        return Qt.ShiftModifier


def get_svg_widget():
    """Get QSvgWidget class with Qt5/Qt6 compatibility"""
    import warnings
    if QT_MAJOR_VERSION >= 6:
        try:
            from qgis.PyQt.QtSvgWidgets import QSvgWidget
            return QSvgWidget
        except ImportError:
            warnings.warn("QSvgWidget could not be imported from qgis.PyQt.QtSvgWidgets (Qt6). SVG icons will not be displayed.")
            return None
    else:
        try:
            from qgis.PyQt.QtSvg import QSvgWidget
            return QSvgWidget
        except ImportError:
            warnings.warn("QSvgWidget could not be imported from qgis.PyQt.QtSvg (Qt5). SVG icons will not be displayed.")
            return None


def get_aspect_ratio_mode():
    """Get Qt.AspectRatioMode for Qt5/Qt6 compatibility"""
    if QT_MAJOR_VERSION >= 6:
        return Qt.AspectRatioMode
    else:
        return Qt

if PY2:
    import urlparse
    from urllib2 import urlopen, URLError
else:
    from urllib import parse

    urlparse = parse
    from urllib.request import urlopen, URLError

if PY3:
    import configparser
else:
    import ConfigParser as configparser


def get_file_dir(filename):
    if PY2:
        return os.path.dirname(filename).decode(sys.getfilesystemencoding())
    else:
        return os.path.dirname(filename)
