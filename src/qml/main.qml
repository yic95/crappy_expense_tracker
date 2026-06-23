import QtQuick
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: appwindow

    function pushEditPage(targetIndex) {
        if (targetIndex === undefined || targetIndex < 0)
            targetIndex = -1;
        else
            targetIndex = expenseProxy.getSourceRow(targetIndex)

        if (applicationWindow().pageStack.depth > 1)
            applicationWindow().pageStack.insertPage(1, Qt.resolvedUrl("EditPage.qml"), {
            "targetRow": targetIndex
        });
        else
            applicationWindow().pageStack.push(Qt.resolvedUrl("EditPage.qml"), {
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

    Kirigami.PromptDialog {
        id: expenseStatsPopup

        QQC2.Label {
            text: "Month: " + expenseModel.getMonthlyExpense()
        }

        QQC2.Label {
            text: "Day: " + expenseModel.getDailyExpense()
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
                            visible: tags.length > 0
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

            QQC2.ActionGroup {
                id: sortGroup
                exclusive: true
            }
            actions: [
                Kirigami.Action {
                    icon.name: "step_object_Graph-symbolic"
                    text: "View Stat"
                    onTriggered: {
                        expenseStatsPopup.open();
                    }
                },
                Kirigami.Action {
                    icon.name: "list-add-symbolic"
                    text: "Add New Entry"
                    onTriggered: {
                        pushEditPage(-1);
                    }
                },
                Kirigami.Action {
                    icon.name: "view-sort-symbolic"
                    text: "Sort"
                    Kirigami.Action {
                        QQC2.ActionGroup.group : sortGroup
                        icon.name: "view-calendar-symbolic"
                        checkable: true
                        text: "Sort by date"
                        checked: true
                        onTriggered: {
                            expenseProxy.sortByDate();
                            expenseListView.section.property =  "date"
                        }
                    }

                    Kirigami.Action {
                        QQC2.ActionGroup.group : sortGroup
                        icon.name: "amarok_playcount-symbolic"
                        checkable: true
                        text: "Sort by expense"
                        checked: false
                        onTriggered: {
                            expenseProxy.sortByExpense();
                            expenseListView.section.property =  "expense"
                        }
                    }
                },
                Kirigami.Action {
                    icon.name: "media-playback-start-symbolic"
                    text: "Play Game"
                    onTriggered: {
                        petLauncher.launch_pet_room();
                    }
                },

            ]

            Connections {
                function onLoadingFailed(errmsg) {
                    expensePage.title = "Expense*";
                }

                target: expenseModel
            }

            Kirigami.CardsListView {
                id: expenseListView

                spacing: Kirigami.Units.largeSpacing
                model: expenseProxy
                delegate: expenseListDelegate
                anchors.fill: parent
                section.property: "date"
                section.delegate: expenseSectionTitle
            }

        }

    }

}
