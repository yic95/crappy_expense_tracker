from PySide6.QtCore import Qt
import enum

class ExpenseRole(enum.IntEnum):
    ROLE_ID = Qt.UserRole + 1
    ROLE_DATE = Qt.UserRole + 2
    ROLE_EXP = Qt.UserRole + 3
    ROLE_TITLE = Qt.UserRole + 4
    ROLE_TAG = Qt.UserRole + 5
