import QtQuick
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami

Kirigami.ScrollablePage {
    id: statPage

    required property int expMonth
    required property int expDay

    ColumnLayout {
        anchors.centerIn: parent
        spacing: Kirigami.Units.largeSpacing

        Kirigami.Heading {
            text: "Month: " + statPage.expMonth
            level: 1
            Layout.alignment: Qt.AlignHCenter
        }

        Kirigami.Heading {
            text: "Day: " + statPage.expDay
            level: 1
            Layout.alignment: Qt.AlignHCenter
        }

    }

}
