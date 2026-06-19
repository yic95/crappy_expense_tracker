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

    function popPage() {
        applicationWindow().pageStack.pop();
    }

    title: isCreateMode ? "Add New Expense" : "Edit Expense"

    Kirigami.PromptDialog {
        id: deleteConfirmationDialog

        title: "Delete Expense?"
        standardButtons: QQC2.Dialog.Yes | QQC2.Dialog.No
        onAccepted: {
            // Invoke your delete routine on the raw model
            expenseModel.remove_expense(getIndex());
            popPage();
        }
        subtitle: "Permanently delete this expense record?"
    }

    Kirigami.FormLayout {
        width: parent.width

        QQC2.TextField {
            id: expenseField

            Kirigami.FormData.label: "Expense: "
            Layout.fillWidth: true
            placeholderText: ""
            inputMethodHints: Qt.ImhDigitsOnly
            Component.onCompleted: {
                if (!editPage.isCreateMode)
                    text = editPage.getModelData("expense").toString();

            }
        }

        QQC2.TextField {
            id: titleField

            Kirigami.FormData.label: "Description"
            Layout.fillWidth: true
            placeholderText: ""
            Component.onCompleted: {
                if (!editPage.isCreateMode)
                    text = editPage.getModelData("title");

            }
        }

        Item {
            Kirigami.FormData.label: "Tags"
            Kirigami.FormData.isSection: true

            Flow {
                // visible: tags !== undefined && tags.length > 0

                id: tagsFlow

                property var activeTags: !editPage.isCreateMode ? (editPage.getModelData("tags")) : []

                Layout.fillWidth: true
                spacing: Kirigami.Units.smallSpacing

                Repeater {
                    model: expenseModel.all_tags

                    delegate: Kirigami.Chip {
                        required property string modelData

                        checked: tagsFlow.activeTags.indexOf(modelData) != -1
                        text: modelData.trim()
                        closable: false
                        onCheckedChanged: {
                            let currentTags = tagsFlow.activeTags.slice(); // Copy JS array safely
                            if (checked) {
                                if (currentTags.indexOf(modelData) === -1)
                                    currentTags.push(modelData);

                            } else {
                                let idx = currentTags.indexOf(modelData);
                                if (idx !== -1)
                                    currentTags.splice(idx, 1);

                            }
                            tagsFlow.activeTags = currentTags;
                        }
                    }

                }

            }

        }

    }

    footer: QQC2.DialogButtonBox {
        QQC2.Button {
            visible: !isCreateMode
            QQC2.DialogButtonBox.buttonRole: QQC2.DialogButtonBox.ActionRole
            icon.name: "delete-symbolic"
            text: "Delete Entry"
            onClicked: {
                deleteConfirmationDialog.open();
            }
        }

        QQC2.Button {
            icon.name: "document-save-symbolic"
            QQC2.DialogButtonBox.buttonRole: QQC2.DialogButtonBox.AcceptRole
            text: "Save"
            onClicked: {
                let amt = parseInt(expenseField.text) || 0;
                if (editPage.isCreateMode)
                    expenseModel.add_expense(editPage.selectedDate, amt, titleField.text, tagsFlow.activeTags);
                else
                    expenseModel.modify_expense(getIndex(), editPage.selectedDate, amt, titleField.text, tagsFlow.activeTags);
                popPage();
            }
        }

        QQC2.Button {
            icon.name: "dialog-cancel-symbolic"
            QQC2.DialogButtonBox.buttonRole: QQC2.DialogButtonBox.RejectRole
            text: "Cancel"
            onClicked: {
                popPage();
            }
        }

    }

}
