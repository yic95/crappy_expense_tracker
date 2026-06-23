from PySide6.QtCore import (
    Qt,
    Signal,
    Property,
    Slot,
    QSortFilterProxyModel,
)

from expensetracker.userroles import ExpenseRole


class ExpenseProxyModel(QSortFilterProxyModel):
    filterTextChanged = Signal()
    sortModeChanged = Signal()

    SORT_DATE = 0
    SORT_EXPENSE = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        self._filter_text = ""
        self._sort_mode = self.SORT_DATE

        self.setDynamicSortFilter(True)
        self.sort(0, Qt.DescendingOrder)

    # ---------- Filtering ----------

    @Property(str, notify=filterTextChanged)
    def filterText(self):
        return self._filter_text

    @filterText.setter
    def filterText(self, text):
        if text == self._filter_text:
            return

        self._filter_text = text
        self.invalidateFilter()
        self.filterTextChanged.emit()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self._filter_text:
            return True

        model = self.sourceModel()

        title_idx = model.index(source_row, 0, source_parent)
        title = model.data(title_idx, ExpenseRole.ROLE_TITLE)

        return self._filter_text.lower() in title.lower()

    @Property(int, notify=sortModeChanged)
    def sortMode(self):
        return self._sort_mode

    @sortMode.setter
    def sortMode(self, mode):
        if mode == self._sort_mode:
            return

        self._sort_mode = mode
        self.invalidate()
        self.sort(0, Qt.DescendingOrder)
        self.sortModeChanged.emit()

    def lessThan(self, left, right):
        model = self.sourceModel()

        if self._sort_mode == self.SORT_EXPENSE:
            l = model.data(left, ExpenseRole.ROLE_EXP)
            r = model.data(right, ExpenseRole.ROLE_EXP)
        else:
            l = model.data(left, ExpenseRole.ROLE_DATE)
            r = model.data(right, ExpenseRole.ROLE_DATE)

        return l < r

    # Convenience slots for QML

    @Slot()
    def sortByDate(self):
        self.sortMode = self.SORT_DATE

    @Slot()
    def sortByExpense(self):
        self.sortMode = self.SORT_EXPENSE

    @Slot(int, result=int)
    def getSourceRow(self, proxy_row: int) -> int:
        return self.mapToSource(self.index(proxy_row, 0)).row()
