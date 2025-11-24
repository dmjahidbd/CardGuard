import platform
import subprocess
from datetime import datetime

class Notifier:
    """
    Cross-platform push notification handler.
    Sends system notifications for updates, blocks, and other important events.
    """
    
    def __init__(self):
        self.platform = platform.system()
        self.notification_history = []
        
    def send_notification(self, title, message, urgency="normal"):
        """
        Send a push notification to the user.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            urgency (str): Urgency level - 'low', 'normal', or 'critical'
        """
        # Log the notification
        notification_data = {
            'timestamp': datetime.now(),
            'title': title,
            'message': message,
            'urgency': urgency
        }
        self.notification_history.append(notification_data)
        
        # Send platform-specific notification
        try:
            if self.platform == "Windows":
                self._send_windows_notification(title, message)
            elif self.platform == "Darwin":  # macOS
                self._send_macos_notification(title, message)
            elif self.platform == "Linux":
                self._send_linux_notification(title, message, urgency)
            else:
                print(f"[NOTIFICATION] {title}: {message}")
        except Exception as e:
            print(f"Failed to send notification: {e}")
            print(f"[NOTIFICATION] {title}: {message}")
            
    def _send_windows_notification(self, title, message):
        """Send notification on Windows using PowerShell."""
        try:
            # Using PyQt6's system tray or Windows toast notifications
            from PyQt6.QtWidgets import QMessageBox
            # For now, we'll use a simple approach
            # In production, you'd use win10toast or similar
            print(f"[WIN NOTIFICATION] {title}: {message}")
        except ImportError:
            print(f"[NOTIFICATION] {title}: {message}")
            
    def _send_macos_notification(self, title, message):
        """Send notification on macOS using osascript."""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=True)
        except Exception as e:
            print(f"[MAC NOTIFICATION] {title}: {message}")
            
    def _send_linux_notification(self, title, message, urgency="normal"):
        """Send notification on Linux using notify-send."""
        try:
            subprocess.run(['notify-send', f'-u', urgency, title, message], check=True)
        except Exception as e:
            print(f"[LINUX NOTIFICATION] {title}: {message}")
            
    def get_notification_history(self):
        """Get all sent notifications."""
        return self.notification_history
    
    def clear_history(self):
        """Clear notification history."""
        self.notification_history.clear()
