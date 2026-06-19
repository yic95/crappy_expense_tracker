import QtQuick
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: appwindow

    function pushEditPage(targetIndex) {
        if (targetIndex === undefined)
            targetIndex = -1;

        applicationWindow().pageStack.push(Qt.resolvedUrl("editPage.qml"), {
            "targetRow": targetIndex
        });
    }

    minimumWidth: Kirigami.Units.gridUnit * 20
    minimumHeight: Kirigami.Units.gridUnit * 30
    width: minimumWidth
    height: minimumHeight
    pageStack.popHiddenPages: true
    pageStack.initialPage: initPage

    Component {
        id: expenseSectionTitle

        Kirigami.ListSectionHeader {
            required property string section

            text: section

            anchors {
                left: parent.left
                right: parent.right
            }

        }

    }

    Component {
        id: expenseListDelegate

        Kirigami.AbstractCard {
            onClicked: {
                pushEditPage(index);
            }
            showClickFeedback: true

            contentItem: Item {
                implicitHeight: delegateLayout.implicitHeight
                implicitWidth: delegateLayout.implicitWidth

                GridLayout {
                    id: delegateLayout

                    rowSpacing: Kirigami.Units.largeSpacing
                    columnSpacing: Kirigami.Units.largeSpacing

                    anchors {
                        left: parent.left
                        right: parent.right
                        top: parent.top
                    }

                    ColumnLayout {
                        Layout.fillWidth: true

                        Kirigami.Heading {
                            Layout.fillWidth: true
                            level: 2
                            text: title
                        }

                        Kirigami.Separator {
                            visible: tags.length > 0
                        }

                        Flow {
                            // visible: tags !== undefined && tags.length > 0

                            Layout.fillWidth: true
                            spacing: Kirigami.Units.smallSpacing

                            Repeater {
                                model: tags

                                delegate: Kirigami.Chip {
                                    required property string modelData

                                    text: modelData.trim()
                                    closable: false
                                    interactive: false
                                }

                            }

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

            Connections {
                function onLoadingFailed(errmsg) {
                    expensePage.title = "Expense*";
                }

                target: expenseModel
            }

            Kirigami.CardsListView {
                id: expenseListView

                spacing: Kirigami.Units.largeSpacing
                model: expenseModel
                delegate: expenseListDelegate
                anchors.fill: parent
                section.property: "date"
                section.delegate: expenseSectionTitle
                onAtYEndChanged: {
                    if (expenseListView.atYEnd)
                        expenseModel.load();

                }
            }

            header: QQC2.ToolBar {

                contentItem: Item {
                    RowLayout {
                        QQC2.Button {
                            onClicked: {
                                pushEditPage(-1);
                            }
                            icon.name: "list-add-symbolic"
                            text: "Add New Entry"
                        }

                        QQC2.ComboBox {
                        }

                    }

                }

            }

        }

    }

}
