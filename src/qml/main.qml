import QtQuick
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    minimumWidth: Kirigami.Units.gridUnit * 20
    minimumHeight: Kirigami.Units.gridUnit * 30
    width: minimumWidth
    height: minimumHeight
    pageStack.initialPage: initPage

    Component {
        id: expenseCard

        Kirigami.AbstractCard {
            onClicked: {
                applicationWindow().pageStack.push(Qt.resolvedUrl("editPage.qml"), {
                    "targetRow": index
                });
            }

            contentItem: Item {
                implicitHeight: delegateLayout.implicitHeight
                implicitWidth: delegateLayout.implicitWidth

                GridLayout {
                    id: delegateLayout

                    rowSpacing: Kirigami.Units.largeSpacing
                    columnSpacing: Kirigami.Units.largeSpacing

                    anchors {
                        left: parent.left
                        // top: parent.top
                        right: parent.right
                    }

                    ColumnLayout {
                        Layout.fillWidth: true

                        Kirigami.Heading {
                            Layout.fillWidth: true
                            level: 2
                            text: title
                        }

                    }

                    Kirigami.Heading {
                        level: 1
                        text: expense
                    }

                }

            }

        }

    }

    Component {
        id: initPage

        Kirigami.ScrollablePage {
            id: expensePage

            verticalScrollBarPolicy: QQC2.ScrollBar.AlwaysOn
            title: "Expenses"
            actions: [
                Kirigami.Action {
                    text: "New Expense"
                    icon.name: "list-add-symbolic"
                    onTriggered: {
                        applicationWindow().pageStack.push(Qt.resolvedUrl("editPage.qml"), {
                            "targetRow": -1
                        });
                    }
                }
            ]

            Connections {
                function onLoadingFailed(errmsg) {
                    expensePage.title = "Expense*";
                }

                target: expenseModel
            }

            ListView {
                id: expenseListView

                anchors.fill: parent
                spacing: Kirigami.Units.largeSpacing
                model: expenseModel
                section.property: "date"
                delegate: expenseCard

                section.delegate: Kirigami.Heading {
                    text: Qt.formatDate(section, "yyyy-MM-dd")
                }

            }

        }

    }

}
