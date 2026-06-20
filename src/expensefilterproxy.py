from PySide6.QtCore import QSortFilterProxyModel, Slot, Qt, QByteArray

class ExpenseFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_category = "All Categories"

        # Default sorting setup (Date role integer)
        self.setDateRole(Qt.UserRole + 1) # Assumed Date Role Enum
        self.setAmountRole(Qt.UserRole + 3) # Assumed Amount/Expense Role Enum

        self.setSortRole(self.DateRole)
        self.sort(0, Qt.DescendingOrder)

    # --- CATEGORY FILTER SLOT ---
    @Slot(str)
    def setCategoryFilter(self, category):
        self._current_category = category
        self.invalidateFilter() # Forces the view to refresh instantly

    def filterAcceptsRow(self, source_row, source_parent):
        # 1. Evaluate your base filter rule
        if self._current_category == "All Categories":
            return True

        source_model = self.sourceModel()
        model_index = source_model.index(source_row, 0, source_parent)

        # Assumed category string lookup role (e.g., Qt.UserRole + 5)
        row_category = source_model.data(model_index, source_model.CategoryRole)
        return row_category == self._current_category

    # --- DYNAMIC SORTING CRITERIA SLOT ---
    @Slot(int)
    def updateSortingCriteria(self, index):
        """Maps ComboBox selection index to specific backend sorting directions."""
        if index == 0: # "Newest First"
            self.setSortRole(self.DateRole)
            self.sort(0, Qt.DescendingOrder)
        elif index == 1: # "Oldest First"
            self.setSortRole(self.DateRole)
            self.sort(0, Qt.AscendingOrder)
        elif index == 2: # "Highest Amount"
            self.setSortRole(self.AmountRole)
            self.sort(0, Qt.DescendingOrder)
        elif index == 3: # "Lowest Amount"
            self.setSortRole(self.AmountRole)
            self.sort(0, Qt.AscendingOrder)
