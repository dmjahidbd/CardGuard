from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QTextEdit, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from utils.notifier import Notifier
from utils.usage_counter import UsageCounter
from utils.block_manager import BlockManager
from hardware.device_handler import DeviceHandler
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardGuard - Secure Card Management")
        self.setGeometry(100, 100, 900, 600)
        
        # Initialize components
        self.notifier = Notifier()
        self.usage_counter = UsageCounter()
        self.block_manager = BlockManager()
        self.device_handler = DeviceHandler()
        
        # Setup UI
        self.init_ui()
        
        # Record usage
        self.usage_counter.increment()
        
        # Check for updates
        self.check_for_updates()
        
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("CardGuard Management System")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Status area
        self.status_label = QLabel("Status: Active")
        self.status_label.setStyleSheet("color: green; font-size: 14px;")
        main_layout.addWidget(self.status_label)
        
        # Usage counter display
        self.usage_display = QLabel(f"Total Usage: {self.usage_counter.get_count()} times")
        main_layout.addWidget(self.usage_display)
        
        # Device status
        self.device_status = QLabel("Device: Not Connected")
        main_layout.addWidget(self.device_status)
        self.update_device_status()
        
        # Log area
        log_label = QLabel("Activity Log:")
        main_layout.addWidget(log_label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        main_layout.addWidget(self.log_area)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("Connect Device")
        self.connect_btn.clicked.connect(self.connect_device)
        button_layout.addWidget(self.connect_btn)
        
        self.scan_btn = QPushButton("Scan Card")
        self.scan_btn.clicked.connect(self.scan_card)
        self.scan_btn.setEnabled(False)
        button_layout.addWidget(self.scan_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(button_layout)
        
        # Security options
        security_layout = QHBoxLayout()
        
        self.block_suspicious_cb = QCheckBox("Block on Suspicious Activity")
        self.block_suspicious_cb.setChecked(True)
        self.block_suspicious_cb.stateChanged.connect(self.toggle_block_mode)
        security_layout.addWidget(self.block_suspicious_cb)
        
        main_layout.addLayout(security_layout)
        
        # Add stretch to push everything to top
        main_layout.addStretch()
        
        # Log initial message
        self.add_log("CardGuard initialized successfully")
        
    def connect_device(self):
        self.add_log("Attempting to connect to device...")
        success = self.device_handler.connect()
        
        if success:
            self.add_log("Device connected successfully")
            self.device_status.setText("Device: Connected")
            self.device_status.setStyleSheet("color: green;")
            self.connect_btn.setText("Disconnect Device")
            self.connect_btn.clicked.disconnect()
            self.connect_btn.clicked.connect(self.disconnect_device)
            self.scan_btn.setEnabled(True)
            self.notifier.send_notification("Device Connected", "Hardware device connected successfully")
        else:
            self.add_log("Failed to connect device")
            QMessageBox.warning(self, "Connection Error", "Failed to connect to device")
            
    def disconnect_device(self):
        self.add_log("Disconnecting device...")
        self.device_handler.disconnect()
        self.device_status.setText("Device: Not Connected")
        self.device_status.setStyleSheet("color: gray;")
        self.connect_btn.setText("Connect Device")
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.connect_device)
        self.scan_btn.setEnabled(False)
        self.add_log("Device disconnected")
        
    def scan_card(self):
        self.add_log("Scanning card...")
        card_data = self.device_handler.scan_card()
        
        if card_data:
            self.add_log(f"Card detected: {card_data}")
            
            # Check for suspicious activity
            if self.block_suspicious_cb.isChecked():
                if self.block_manager.is_suspicious(card_data):
                    self.add_log("WARNING: Suspicious activity detected!")
                    self.status_label.setText("Status: Blocked - Suspicious Activity")
                    self.status_label.setStyleSheet("color: red; font-size: 14px;")
                    QMessageBox.critical(self, "Security Alert", "Suspicious activity detected! Operation blocked.")
                    self.notifier.send_notification("Security Alert", "Suspicious card activity detected")
                    return
            
            self.add_log("Card scan completed successfully")
            QMessageBox.information(self, "Scan Complete", f"Card scanned successfully\nData: {card_data}")
        else:
            self.add_log("No card detected")
            QMessageBox.warning(self, "Scan Error", "No card detected. Please try again.")
            
    def refresh_data(self):
        self.add_log("Refreshing data...")
        self.usage_display.setText(f"Total Usage: {self.usage_counter.get_count()} times")
        self.update_device_status()
        self.add_log("Data refreshed")
        
    def update_device_status(self):
        if self.device_handler.is_connected():
            self.device_status.setText("Device: Connected")
            self.device_status.setStyleSheet("color: green;")
        else:
            self.device_status.setText("Device: Not Connected")
            self.device_status.setStyleSheet("color: gray;")
            
    def toggle_block_mode(self, state):
        if state == Qt.CheckState.Checked.value:
            self.add_log("Block on suspicious activity: ENABLED")
            self.notifier.send_notification("Security Mode", "Blocking enabled for suspicious activity")
        else:
            self.add_log("Block on suspicious activity: DISABLED")
            self.notifier.send_notification("Security Mode", "Blocking disabled")
            
    def check_for_updates(self):
        # Simulate version check
        current_version = "1.0.0"
        self.add_log(f"Current version: {current_version}")
        # In real implementation, this would check a remote server
        # For now, just log that we checked
        self.add_log("Checked for updates - Up to date")
        
    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        # Clean disconnect on close
        if self.device_handler.is_connected():
            self.device_handler.disconnect()
        event.accept()
