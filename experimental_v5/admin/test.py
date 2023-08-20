import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget

class SearchHistoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search History Example")
        self.setGeometry(100, 100, 300, 200)
        
        self.init_ui()
        
    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        
        self.combo_box = QComboBox(self)
        self.load_search_history()
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)
        
        layout.addWidget(self.combo_box)
        self.central_widget.setLayout(layout)
        
    def load_search_history(self):
        self.combo_box.clear()
        self.combo_box.addItem("Select a search...")
        
        search_history = [
            "John Smith",
            "Jane Doe",
            "Michael Johnson",
            "Emily Brown",
            # Add more names as needed
        ]
        
        for name in search_history:
            self.combo_box.addItem(name)
    
    def combo_box_changed(self, index):
        selected_name = self.combo_box.currentText()
        if selected_name != "Select a search...":
            print(f"Selected Name: {selected_name}")
            # Perform further actions based on the selected name
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchHistoryApp()
    window.show()
    sys.exit(app.exec())
