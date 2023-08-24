import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QFrame

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create the header layout (QVBoxLayout)
        header_layout = QVBoxLayout()

        # Create an embossed effect using a QFrame
        embossed_frame = QFrame()
        embossed_frame.setStyleSheet("QFrame { border: 10px solid gray; border-radius: 25px; margin: 0.5em; background-color: #F0F0F0; }")
        header_layout.addWidget(embossed_frame)

        header_label = QLabel("Header")
        header_layout.addWidget(header_label)

        # Create the details layout (QFormLayout)
        details_layout = QFormLayout()
        details_layout.addRow("Name:", QLineEdit())
        details_layout.addRow("Age:", QLineEdit())
        details_layout.addRow("Email:", QLineEdit())

        # Create the main layout and add the header and details layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addLayout(details_layout)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
