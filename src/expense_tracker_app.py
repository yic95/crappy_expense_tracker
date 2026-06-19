#!/usr/bin/env python3

import os
import sys
import signal
import pathlib
import appdirs
import json

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from expensemodel import ExpenseModel
from expenseservice import ExpenseService
from tagsservice import TagsService


def get_config():
    appname = 'ExpenseTracker'
    appauthor = 'Yichm'
    app_data_dir = pathlib.Path(appdirs.user_data_dir(appname, appauthor))
    expense_dir_file = app_data_dir / 'settings.json'
    result = {}
    with expense_dir_file.open('r', encoding='utf-8', newline='') as f:
        result = json.load(f)
    return result


def main():
    """Initializes and manages the application execution"""
    config = get_config()
    data_dir = ""
    if 'data_dir' in config:
        data_dir = config['data_dir']
    app = QGuiApplication(sys.argv)
    QGuiApplication.setApplicationName("Expense Tracker")
    engine = QQmlApplicationEngine()
    expense_service = ExpenseService(data_dir)
    tags_service = TagsService(data_dir)
    expense_model = ExpenseModel(service=expense_service, tags_service=tags_service)

    """Needed to get proper KDE style outside of Plasma"""
    if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    """Needed to close the app with Ctrl+C"""
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    base_path = os.path.abspath(os.path.dirname(__file__))
    url = QUrl(f"file://{base_path}/qml/main.qml")
    engine.rootContext().setContextProperty("expenseModel", expense_model)
    engine.load(url)

    if len(engine.rootObjects()) == 0:
        quit()

    app.exec()


if __name__ == "__main__":
    main()
