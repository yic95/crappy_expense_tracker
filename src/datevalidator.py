from PySide6.QtGui import QValidator

from datetime import date
from PySide6.QtCore import (
    QDate,
    Qt,
    Slot,
    Signal,
    Property,
)

class DateValidator(QValidator):
    def __init__(self, parent=None):
        super().__init__(parent)

    def fixup(self, string: str):
        strip_str = string.strip()
        sep_symbol_set = {c for c in strip_str if not c.isdigit()}
        if len(sep_symbol_set) != 1:
            return strip_str
        (sep_symbol,) = sep_symbol_set
        if len(strip_str.split(sep_symbol)) != 3:
            return strip_str.replace(sep_symbol, '-', -1)
        try:
            date.strptime(strip_str, f"%Y{sep_symbol}%m{sep_symbol}%d")
            return strip_str.replace(sep_symbol, '-', -1)
        except:
            pass
        try:
            date.strptime(strip_str[:-1:], f"%Y{sep_symbol}%m{sep_symbol}%d")
            return strip_str[:-1:].replace(sep_symbol, '-', -1)
        except:
            return strip_str.replace(sep_symbol, '-', -1)

    def validate(self, string: str, position: int):
        strip_str = string.strip()
        if len(strip_str) > 10:
            return self.State.Invalid
        sep_symbol_set = {c for c in strip_str if not c.isdigit()}
        if len(sep_symbol_set) > 1:
            return self.State.Invalid
        if len(sep_symbol_set) == 0:
            if len(strip_str) <= 4:
                return self.State.Intermediate
            return self.State.Invalid
        (sep_symbol,) = sep_symbol_set
        if len(strip_str.split(sep_symbol)) > 3:
            return self.State.Invalid
        if len(strip_str) < 10:
            return self.State.Intermediate
        try:
            date.strptime(string, f"%Y{sep_symbol}%m{sep_symbol}%d")
            if sep_symbol == '-':
                return self.State.Acceptable
            return self.State.Intermediate
        except:
            pass

        try:
            date.strptime(strip_str, f"%Y{sep_symbol}%m{sep_symbol}%d")
            return self.State.Intermediate
        except:
            return self.State.Invalid
