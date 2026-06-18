import QtQuick
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami

Kirigami.ScrollablePage {
    id: editPage

    property int targetRow: -1
    readonly property bool isCreateMode: targetRow === -1
    property var selectedDate: !isCreateMode ? getModelData("date") : new Date()

    // Helper functions to fetch data directly from the model using the targetRow index
    function getModelData(roleName) {
        if (isCreateMode)
            return null;

        let result = expenseModel.data(getIndex(), expenseModel.get_role(roleName));
        return result;
    }

    function getIndex() {
        return expenseModel.index(targetRow, 0);
    }

    title: isCreateMode ? "Add New Expense" : "Edit Expense"

    ColumnLayout {
        width: parent.width
        spacing: Kirigami.Units.largeSpacing

        QQC2.Label {
            text: "Expense"
            font.bold: true
        }

        QQC2.TextField {
            id: expenseField

            Layout.fillWidth: true
            placeholderText: ""
            inputMethodHints: Qt.ImhDigitsOnly
            Component.onCompleted: {
                if (!editPage.isCreateMode)
                    text = editPage.getModelData("expense").toString();

            }
        }

        QQC2.Label {
            text: "Description"
            font.bold: true
        }

        QQC2.TextArea {
            id: titleArea

            Layout.fillWidth: true
            placeholderText: ""
            Component.onCompleted: {
                if (!editPage.isCreateMode)
                    text = editPage.getModelData("title");

            }
        }

    }

    footer: QQC2.DialogButtonBox {
        standardButtons: QQC2.DialogButtonBox.Ok | QQC2.DialogButtonBox.Cancel
        onAccepted: {
            let amt = parseInt(expenseField.text) || 0;
            if (editPage.isCreateMode) {
                // Call the model's add_expense slot directly
                expenseModel.add_expense(editPage.selectedDate, amt, titleArea.text);
            } else {
                // Generate the proper QModelIndex and update the model
                let modelIndex = expenseModel.index(editPage.targetRow, 0);
                expenseModel.modify_expense(modelIndex, editPage.selectedDate, amt, titleArea.text);
            }
            applicationWindow().pageStack.pop();
        }
        onRejected: {
            applicationWindow().pageStack.pop();
        }
    }

}
