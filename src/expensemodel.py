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
    TagsRole = Qt.UserRole + 5
    loadingFailed = Signal(str)
    hasMoreChanged = Signal(bool)

    def __init__(self, parent=None,*, service=None):
        super().__init__(parent)
        self.entries = []
        self.service = service
        self.earlist_date = None
        self.batch_size_day = 7
        self._has_more_data = True

    @Property(bool, notify=hasMoreChanged)
    def hasMore(self):
        return self._has_more_data

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
        if role == self.TagsRole:
            return row['tags']
        print("...")
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
        if name == 'tags':
            return self.TagsRole

    def roleNames(self):
        return {
            self.IdRole: QByteArray(b"id"),
            self.DateRole: QByteArray(b"date"),
            self.ExpenseRole: QByteArray(b"expense"),
            self.TitleRole: QByteArray(b"title"),
            self.TagsRole: QByteArray(b"tags")
        }

    @Slot(QDate, int, str)
    def add_expense(self, date: QDate, expense: int, title: str, tags: list[str]):
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

    @Slot(QModelIndex)
    def remove_expense(self, idx: QModelIndex):
        row = self.entries[idx.row()]
        self.service.delete(row['date'].toPython(), row['id'])
        self.beginRemoveRows(QModelIndex(), idx.row(), idx.row())
        self.entries.pop(idx.row())
        self.endRemoveRows()

    @Slot(QModelIndex, QDate, int, str)
    def modify_expense(self, idx: QModelIndex, date: QDate, expense: int, title: str, tags: list[str]):
        if not idx.isValid():
            return None
        row = self.entries[idx.row()]
        self.service.update({
            'date': date.toPython(),
            'id': row['id'],
            'expense': expense,
            'title': title,
            'tags': tags})
        row['expense'] = expense
        row['title'] = title
        row['date'] = date
        row['tags'] = tags
        self.dataChanged.emit(idx, idx)

    @Slot()
    def load(self):
        new_entries = []
        if not self.earlist_date:
            self.earlist_date = datetime.date.today()
        try:
            new_entries = self.service.read(self.earlist_date - datetime.timedelta(self.batch_size_day), self.earlist_date)
            if new_entries:
                self.earlist_date = self.earlist_date - datetime.timedelta(self.batch_size_day + 1)
        except Exception as e:
            print(e)
            self.loadingFailed.emit(f"Fail to load budget file: {str(e)}")
        for row in new_entries:
            row['date'] = QDate(row['date'].year, row['date'].month, row['date'].day)
        new_entries.sort(reverse=True, key=lambda d: d['date'])

        if new_entries:
            self.beginInsertRows(QModelIndex(), len(self.entries), len(self.entries) + len(new_entries) - 1)
            self.entries.extend(new_entries)
            self.endInsertRows()
