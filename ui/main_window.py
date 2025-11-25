from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QListWidget,
                             QTextEdit, QMessageBox, QTabWidget, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from utils.notifier import Notifier
from utils.usage_counter import UsageCounter
from utils.app_locker import AppLocker
from hardware.card_reader import CardReader
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardGuard - Application Locker")
        self.setGeometry(100, 100, 900, 700)
        
        # Initialize components
        self.notifier = Notifier()
        self.usage_counter = UsageCounter()
        self.app_locker = AppLocker()
        self.card_reader = CardReader()
        
        # Setup UI
        self.init_ui()
        
        # Record usage
        self.usage_counter.increment()
        
        # Start card monitoring
        self.start_card_monitoring()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("CardGuard - Lock Your Applications")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget for different sections
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Setup Tab
        self.setup_tab = self.create_setup_tab()
        self.tabs.addTab(self.setup_tab, "Card Setup")
        
        # Lock Tab
        self.lock_tab = self.create_lock_tab()
        self.tabs.addTab(self.lock_tab, "Lock Applications")
        
        # Status Tab
        self.status_tab = self.create_status_tab()
        self.tabs.addTab(self.status_tab, "Status & Logs")
        
    def create_setup_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Card Registration Section
        reg_label = QLabel("Step 1: Register Your Card")
        reg_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(reg_label)
        
        self.card_status_label = QLabel("No card registered")
        layout.addWidget(self.card_status_label)
        
        reg_btn_layout = QHBoxLayout()
        self.register_card_btn = QPushButton("Register Card")
        self.register_card_btn.clicked.connect(self.register_card)
        reg_btn_layout.addWidget(self.register_card_btn)
        
        self.remove_card_btn = QPushButton("Remove Card")
        self.remove_card_btn.clicked.connect(self.remove_card)
        self.remove_card_btn.setEnabled(False)
        reg_btn_layout.addWidget(self.remove_card_btn)
        layout.addLayout(reg_btn_layout)
        
        # PIN Setup Section
        pin_label = QLabel("Step 2: Set PIN (Optional)")
        pin_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(pin_label)
        
        pin_layout = QHBoxLayout()
        pin_layout.addWidget(QLabel("PIN:"))
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(6)
        pin_layout.addWidget(self.pin_input)
        
        self.set_pin_btn = QPushButton("Set PIN")
        self.set_pin_btn.clicked.connect(self.set_pin)
        pin_layout.addWidget(self.set_pin_btn)
        layout.addLayout(pin_layout)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_lock_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Select Applications to Lock:")
        info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(info_label)
        
        # Application list
        self.app_list = QListWidget()
        self.load_applications()
        layout.addWidget(self.app_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.lock_apps_btn = QPushButton("Lock Selected Apps")
        self.lock_apps_btn.clicked.connect(self.lock_applications)
        btn_layout.addWidget(self.lock_apps_btn)
        
        self.unlock_apps_btn = QPushButton("Unlock All Apps")
        self.unlock_apps_btn.clicked.connect(self.unlock_applications)
        btn_layout.addWidget(self.unlock_apps_btn)
        
        self.refresh_apps_btn = QPushButton("Refresh List")
        self.refresh_apps_btn.clicked.connect(self.load_applications)
        btn_layout.addWidget(self.refresh_apps_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
        
    def create_status_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Status display
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Lock Status:"))
        self.lock_status_label = QLabel("Unlocked")
        self.lock_status_label.setStyleSheet("color: green; font-weight: bold;")
        status_layout.addWidget(self.lock_status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Card status
        card_layout = QHBoxLayout()
        card_layout.addWidget(QLabel("Card Status:"))
        self.card_detect_label = QLabel("Not detected")
        card_layout.addWidget(self.card_detect_label)
        card_layout.addStretch()
        layout.addLayout(card_layout)
        
        # Usage counter
        self.usage_label = QLabel(f"App Usage: {self.usage_counter.get_count()} times")
        layout.addWidget(self.usage_label)
        
        # Activity log
        log_label = QLabel("Activity Log:")
        layout.addWidget(log_label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        self.add_log("CardGuard initialized")
        
        widget.setLayout(layout)
        return widget
        
    def register_card(self):
        self.add_log("Insert your card to register...")
        QMessageBox.information(self, "Register Card", "Please insert your card now")
        
        card_id = self.card_reader.read_card()
        if card_id:
            self.app_locker.register_card(card_id)
            self.card_status_label.setText(f"Card registered: {card_id[:8]}...")
            self.register_card_btn.setEnabled(False)
            self.remove_card_btn.setEnabled(True)
            self.add_log(f"Card registered successfully")
            self.notifier.send_notification("Card Registered", "Your card has been registered with CardGuard")
        else:
            QMessageBox.warning(self, "Error", "Failed to read card. Please try again.")
            self.add_log("Card registration failed")
            
    def remove_card(self):
        reply = QMessageBox.question(self, 'Remove Card', 
                                    'Are you sure you want to remove the registered card?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.app_locker.remove_card()
            self.card_status_label.setText("No card registered")
            self.register_card_btn.setEnabled(True)
            self.remove_card_btn.setEnabled(False)
            self.add_log("Card removed")
            
    def set_pin(self):
        pin = self.pin_input.text()
        if len(pin) >= 4:
            self.app_locker.set_pin(pin)
            self.add_log("PIN set successfully")
            QMessageBox.information(self, "PIN Set", "Your PIN has been set")
            self.pin_input.clear()
        else:
            QMessageBox.warning(self, "Invalid PIN", "PIN must be at least 4 digits")
            
    def load_applications(self):
        self.app_list.clear()
        apps = self.app_locker.get_installed_apps()
        for app in apps:
            # Extract app name with fallback to handle dict objects
            try:
                if isinstance(app, dict):
                    app_name = app.get('name', str(app))
                else:
                    app_name = str(app)
                self.app_list.addItem(app_name)
            except Exception as e:
                self.add_log(f"Error loading app: {e}")        self.add_log(f"Loaded {len(apps)} applications")
        
    def lock_applications(self):
        selected_items = self.app_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select apps to lock")
            return
            
        app_names = [item.text() for item in selected_items]
        self.app_locker.lock_apps(app_names)
        self.lock_status_label.setText("Locked")
        self.lock_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.add_log(f"Locked {len(app_names)} applications")
        self.notifier.send_notification("Apps Locked", f"{len(app_names)} applications are now locked")
        
    def unlock_applications(self):
        if not self.app_locker.is_card_registered():
            QMessageBox.warning(self, "No Card", "Please register a card first")
            return
            
        # Read card
        card_id = self.card_reader.read_card()
        if card_id and self.app_locker.verify_card(card_id):
            # Check PIN if set
            if self.app_locker.has_pin():
                pin, ok = QLineEdit.getText(self, "Enter PIN", "Enter your PIN:")
                if not ok or not self.app_locker.verify_pin(pin):
                    QMessageBox.critical(self, "Wrong PIN", "Incorrect PIN")
                    self.add_log("Unlock failed - wrong PIN")
                    return
                    
            self.app_locker.unlock_all_apps()
            self.lock_status_label.setText("Unlocked")
            self.lock_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.add_log("All applications unlocked")
            self.notifier.send_notification("Apps Unlocked", "Applications are now unlocked")
        else:
            QMessageBox.critical(self, "Card Error", "Invalid card or card not detected")
            self.add_log("Unlock failed - invalid card")
            
    def start_card_monitoring(self):
        self.card_timer = QTimer()
        self.card_timer.timeout.connect(self.check_card_presence)
        self.card_timer.start(1000)  # Check every second
        
    def check_card_presence(self):
        if self.card_reader.is_card_present():
            self.card_detect_label.setText("Card detected")
            self.card_detect_label.setStyleSheet("color: green;")
        else:
            self.card_detect_label.setText("No card detected")
            self.card_detect_label.setStyleSheet("color: gray;")
            
    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        # Clean up
        if hasattr(self, 'card_timer'):
            self.card_timer.stop()
        event.accept()
