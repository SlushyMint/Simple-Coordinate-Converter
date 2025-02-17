from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import sys
import folium
import os
import tempfile

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coordinate Converter with Live Map")
        self.setGeometry(100, 100, 900, 700)

        # Set dark theme
        self.set_dark_theme()

        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)  
        self.layout.setSpacing(20)  

        # Title Label
        title_label = QLabel("Coordinate Converter")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(title_label)

        # Latitude input
        lat_frame = QFrame()
        lat_layout = QVBoxLayout(lat_frame)
        lat_layout.setContentsMargins(0, 0, 0, 0)
        lat_label = QLabel("Latitude (-90 to 90)")
        lat_label.setFont(QFont("Segoe UI", 12))
        lat_label.setStyleSheet("color: #ffffff;")
        self.lat_input = QLineEdit()
        self.lat_input.setPlaceholderText("Enter latitude")
        self.lat_input.setFont(QFont("Segoe UI", 12))
        self.lat_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.lat_input.setFixedWidth(300)
        lat_layout.addWidget(lat_label)
        lat_layout.addWidget(self.lat_input)
        self.layout.addWidget(lat_frame, alignment=Qt.AlignCenter)

        # Longitude input
        long_frame = QFrame()
        long_layout = QVBoxLayout(long_frame)
        long_layout.setContentsMargins(0, 0, 0, 0)
        long_label = QLabel("Longitude (-180 to 180)")
        long_label.setFont(QFont("Segoe UI", 12))
        long_label.setStyleSheet("color: #ffffff;")
        self.long_input = QLineEdit()
        self.long_input.setPlaceholderText("Enter longitude")
        self.long_input.setFont(QFont("Segoe UI", 12))
        self.long_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.long_input.setFixedWidth(300)
        long_layout.addWidget(long_label)
        long_layout.addWidget(self.long_input)
        self.layout.addWidget(long_frame, alignment=Qt.AlignCenter)

        # Show Map button
        self.show_map_button = QPushButton("Show Map")
        self.show_map_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.show_map_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.show_map_button.clicked.connect(self.show_live_map)
        self.layout.addWidget(self.show_map_button, alignment=Qt.AlignCenter)

        # WebView for displaying the map
        self.browser = QWebEngineView()
        self.browser.setFixedSize(800, 400)
        self.browser.setStyleSheet("background-color: #1e1e1e;")
        self.layout.addWidget(self.browser, alignment=Qt.AlignCenter)

    def set_dark_theme(self):
        # Apply a dark theme for the application
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)

    def show_live_map(self):
        try:
            lat = self.lat_input.text().strip()
            long = self.long_input.text().strip()

            if not lat or not long:
                return

            lat = float(lat)
            long = float(long)

            # Validate coordinates
            if not -90 <= lat <= 90:
                raise ValueError("Latitude must be between -90 and 90 degrees")
            if not -180 <= long <= 180:
                raise ValueError("Longitude must be between -180 and 180 degrees")

            # Generate the Folium map
            m = folium.Map(location=[lat, long], zoom_start=13)
            folium.Marker([lat, long], popup=f"Lat: {lat}, Long: {long}").add_to(m)

            # Save the map as an HTML file
            temp_dir = tempfile.gettempdir()
            map_file = os.path.join(temp_dir, "location_map.html")
            m.save(map_file)

            # Load the map into the WebView
            self.browser.setUrl(QUrl.fromLocalFile(map_file))
        except ValueError as e:
            print(f"Invalid input: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())