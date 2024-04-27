import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # configure window
        self.setWindowTitle("Team PhotoLab")
        self.setGeometry(100, 100, 1920, 1080)  # x, y, width, height

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)

        # configure grid layout (4x4)
        self.grid_layout.setColumnStretch(1, 1)  # Allow column 1 to expand
        self.grid_layout.setRowStretch(0, 1)  # All rows can expand

        # create sidebar with widgets
        self.sidebar_frame = QFrame(self)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.grid_layout.addWidget(
            self.sidebar_frame, 0, 0, 4, 1)  # spans all 4 rows
        self.logo_label = QLabel("PoseFit Trainer", self.sidebar_frame)
        self.logo_label.setWordWrap(True)
        self.sidebar_layout.addWidget(self.logo_label)

        # Radiobuttons
        self.radio_group = QButtonGroup(self.sidebar_frame)
        self.squat_radio = QRadioButton("Squat", self.sidebar_frame)
        self.radio_group.addButton(self.squat_radio, 0)
        self.pullup_radio = QRadioButton("Pullup", self.sidebar_frame)
        self.radio_group.addButton(self.pullup_radio, 1)
        self.pushup_radio = QRadioButton("Pushup", self.sidebar_frame)
        self.radio_group.addButton(self.pushup_radio, 2)
        self.sidebar_layout.addWidget(self.squat_radio)
        self.sidebar_layout.addWidget(self.pullup_radio)
        self.sidebar_layout.addWidget(self.pushup_radio)

        # Image
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap("logo.png")
        self.image_label.setPixmap(
            self.image_pixmap.scaled(1200, 740, Qt.KeepAspectRatio))
        # spans 4 rows and 3 columns
        self.grid_layout.addWidget(self.image_label, 0, 1, 4, 3)

        # connect events
        self.squat_radio.clicked.connect(self.squat_event)
        self.pullup_radio.clicked.connect(self.pullup_event)
        self.pushup_radio.clicked.connect(self.pushup_event)

    def squat_event(self):
        self.image_label.setPixmap(
            QPixmap("test_image.jpg").scaled(1200, 740, Qt.KeepAspectRatio))
        print("You're squatting right now, we will watch over your form!\n")

    def pullup_event(self):
        self.image_label.setPixmap(
            QPixmap("test_image_1.jpg").scaled(1200, 740, Qt.KeepAspectRatio))

    def pushup_event(self):
        self.image_label.setPixmap(
            QPixmap("test_image_1.jpg").scaled(1200, 740, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
