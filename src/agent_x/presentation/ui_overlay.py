import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from src.agent_x.application.ports.interfaces import ISummaryPresenter
from src.agent_x.application.dto.requests import UIUpdateViewModel

class PyQtPresenter(QWidget):
    """A floating, always-on-top overlay for Wayland/Ubuntu desktops."""
    
    def __init__(self):
        super().__init__()
        # Set window to float on top and remove standard borders
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("StealthCopilot: Active and listening...")
        self.label.setStyleSheet("""
            color: #00FF00; 
            background-color: rgba(20, 20, 20, 220); 
            padding: 15px; 
            border-radius: 8px;
            font-family: monospace;
            font-size: 14px;
        """)
        self.label.setWordWrap(True)
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        # Position it in the top-right corner of the screen
        self.setGeometry(1400, 50, 450, 150)

    def display_summary(self, view_model: UIUpdateViewModel) -> None:
        """Pushes the generated AI response to the UI."""
        self.label.setText(f"[{view_model.system_status.upper()}]\n{view_model.formatted_summary}")
