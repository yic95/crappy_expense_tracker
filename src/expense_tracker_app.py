#!/usr/bin/env python3

import os
import sys
import signal

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from expensemodel import ExpenseModel
from expenseservice import ExpenseService


def main():
    """Initializes and manages the application execution"""
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    expense_service = ExpenseService('/home/yichm/Sync/budget/')
    expense_model = ExpenseModel(service=expense_service)

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

    expense_model.load()
    app.exec()


if __name__ == "__main__":
    main()
