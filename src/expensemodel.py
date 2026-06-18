import pathlib
import csv
import datetime
from PySide6.QtCore import (
    QDate,
    Qt,
    QAbstractListModel,
    QModelIndex,
    QByteArray,
    Slot,
    Signal,
    Property
)
from PySide6.QtQml import QmlElement

class ExpenseModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    DateRole = Qt.UserRole + 2
    ExpenseRole = Qt.UserRole + 3
    TitleRole = Qt.UserRole + 4
    loadingFailed = Signal(str)

    def __init__(self, parent=None,*, service=None):
        super().__init__(parent)
        self.entries = []
        self.service = service

    def rowCount(self, parent=QModelIndex()):
        return len(self.entries)

    def data(self, index, role):
        if type(role) != int:
            raise TypeError
        if not index.isValid():
            return None

        row = self.entries[index.row()]
        if role == self.IdRole:
            return row['id']
        if role == self.DateRole:
            return row['date']
        if role == self.ExpenseRole:
            return row['expense']
        if role == self.TitleRole:
            return row['title']
        print("...")
        return None

    @Slot(int, result=str)
    def data_title(self, index):
        try:
            return self.entries[index]['title']
        except KeyError:
            return None

    @Slot(str, result=int)
    def get_role(self, name):
        if name == 'id':
            return self.IdRole
        if name == 'expense':
            return self.ExpenseRole
        if name == 'date':
            return self.DateRole
        if name == 'title':
            return self.TitleRole

    def roleNames(self):
        return {
            self.IdRole: QByteArray(b"id"),
            self.DateRole: QByteArray(b"date"),
            self.ExpenseRole: QByteArray(b"expense"),
            self.TitleRole: QByteArray(b"title"),
        }

    @Slot(QDate, int, str)
    def add_expense(self, date: QDate, expense: int, title: str):
        max_info = (-1, 0)
        try:
            max_info = max([
                (idx, row['id'])
                    for idx, row in enumerate(self.entries)
                    if row['date'] == date],
                key=lambda pair: pair[1])
        except ValueError:
            pass
        new_entry = {'date': date.toPython(), 'id': max_info[1] + 1, 'expense': expense, 'title': title}
        self.service.write(new_entry)
        new_entry['date'] = date
        self.beginInsertRows(QModelIndex(), max_info[0] + 1, max_info[0] + 1)
        self.entries.insert(max_info[0] + 1, new_entry)
        self.endInsertRows()

    @Slot(QModelIndex, QDate, int, str)
    def modify_expense(self, idx: QModelIndex, date: QDate, expense: int, title: str):
        if not idx.isValid():
            return None
        row = self.entries[idx.row()]
        self.service.update({
            'date': row['date'].toPython(),
            'id': row['id'],
            'expense': row['expense'],
            'title': row['title']})
        row['expense'] = expense
        row['title'] = title
        row['date'] = date
        self.dataChanged.emit(idx, idx)
    
    @Slot()
    def load(self):
        entries = []
        try:
            entries = self.service.read(datetime.date.today() - datetime.timedelta(30), datetime.date.today())
        except Exception as e:
            print(e)
            self.loadingFailed.emit(f"Fail to load budget file: {str(e)}")
        for row in entries:
            row['date'] = QDate(row['date'].year, row['date'].month, row['date'].day)
        entries.sort(reverse=True, key=lambda d: d['date'])

        self.beginResetModel()
        self.entries = entries
        self.endResetModel()
