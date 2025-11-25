import time
import random
from typing import Optional, Dict

class CardReader:
    """Hardware interface for NFC/RFID card reader"""
    
    def __init__(self):
        self.card_present = False
        self.last_card_id = None
        
    def read_card(self) -> Optional[str]:
        """Read card ID from reader. Returns None if no card present."""
        # Simulate card reading with random ID for demo
        if random.random() < 0.3:  # 30% chance of card being present
            self.card_present = True
            self.last_card_id = f"CARD-{random.randint(1000, 9999)}"
            return self.last_card_id
        return None
    
    def is_card_present(self) -> bool:
        """Check if card is currently present"""
        return self.card_present
    
    def wait_for_card(self, timeout=10):
        """Wait for card to be inserted. Returns card ID or None on timeout."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_card_present():
                return self.read_card()
            time.sleep(0.1)
        return None
    
    def eject_card(self):
        """Simulate card ejection"""
        self.card_present = False
        self.last_card_id = None
    
    def get_card_info(self) -> Dict:
        """Get information about currently inserted card"""
        if not self.last_card_id:
            return {}
        return {
            'card_id': self.last_card_id,
            'type': 'NFC',
            'status': 'active' if self.card_present else 'removed'
        }
