import time
import random

class DeviceHandler:
    """
    Handles hardware device integration for card scanning.
    Provides simulated and real hardware connectivity.
    """
    
    def __init__(self):
        self.connected = False
        self.device_info = None
        self.last_scan_time = None
        
    def connect(self):
        """
        Connect to hardware device.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Simulate device connection
            # In a real implementation, this would connect to actual hardware
            time.sleep(0.5)  # Simulate connection delay
            
            # For demo purposes, simulate successful connection
            self.connected = True
            self.device_info = {
                'name': 'CardGuard Scanner',
                'model': 'CG-1000',
                'version': '1.0.0',
                'serial': 'CG' + str(random.randint(100000, 999999))
            }
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
            return False
            
    def disconnect(self):
        """Disconnect from hardware device."""
        self.connected = False
        self.device_info = None
        
    def is_connected(self):
        """Check if device is connected."""
        return self.connected
        
    def scan_card(self):
        """
        Scan a card using the hardware device.
        
        Returns:
            str: Card data if successful, None otherwise
        """
        if not self.connected:
            print("Device not connected")
            return None
            
        try:
            # Simulate card scanning
            time.sleep(1)  # Simulate scan time
            
            # For demo purposes, generate simulated card data
            # In real implementation, this would read from actual hardware
            card_types = ['VALID', 'VALID', 'VALID', 'INVALID']  # 75% valid
            card_type = random.choice(card_types)
            
            if card_type == 'VALID':
                card_data = f"CARD-{random.randint(10000000, 99999999)}"
            else:
                card_data = "INVALID-CARD-DATA"
                
            self.last_scan_time = time.time()
            return card_data
            
        except Exception as e:
            print(f"Scan error: {e}")
            return None
            
    def get_device_info(self):
        """Get connected device information."""
        return self.device_info
        
    def test_device(self):
        """
        Test device connectivity and functionality.
        
        Returns:
            dict: Test results
        """
        results = {
            'connection': self.is_connected(),
            'device_info': self.device_info,
            'last_scan': self.last_scan_time
        }
        
        if self.connected:
            # Perform a test scan
            test_data = self.scan_card()
            results['test_scan'] = test_data is not None
            
        return results
