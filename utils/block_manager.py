import json
import hashlib
from datetime import datetime
from pathlib import Path

class BlockManager:
    """
    Manages blocking functionality for suspicious card activity.
    Maintains a blacklist and suspicious pattern detection.
    """
    
    def __init__(self, blacklist_file="blacklist.json"):
        self.data_dir = Path.home() / ".cardguard"
        self.data_dir.mkdir(exist_ok=True)
        self.blacklist_file = self.data_dir / blacklist_file
        self.blacklist = self._load_blacklist()
        self.suspicious_patterns = self._load_suspicious_patterns()
        
    def _load_blacklist(self):
        """Load blacklist from file."""
        if self.blacklist_file.exists():
            try:
                with open(self.blacklist_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading blacklist: {e}")
                return {'blocked_cards': [], 'blocked_patterns': []}
        else:
            return {'blocked_cards': [], 'blocked_patterns': []}
            
    def _save_blacklist(self):
        """Save blacklist to file."""
        try:
            with open(self.blacklist_file, 'w') as f:
                json.dump(self.blacklist, f, indent=4)
        except Exception as e:
            print(f"Error saving blacklist: {e}")
            
    def _load_suspicious_patterns(self):
        """Load predefined suspicious patterns."""
        return [
            'INVALID',
            'ERROR',
            'CORRUPT',
            'MALFORMED',
            '00000000',
            'FFFFFFFF'
        ]
        
    def is_suspicious(self, card_data):
        """
        Check if card data appears suspicious.
        
        Args:
            card_data (str): Card data to check
            
        Returns:
            bool: True if suspicious, False otherwise
        """
        if not card_data:
            return True
            
        card_data_upper = str(card_data).upper()
        
        # Check against blacklist
        card_hash = hashlib.sha256(card_data.encode()).hexdigest()
        if card_hash in self.blacklist['blocked_cards']:
            return True
            
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if pattern in card_data_upper:
                return True
                
        for pattern in self.blacklist['blocked_patterns']:
            if pattern.upper() in card_data_upper:
                return True
                
        return False
        
    def add_to_blacklist(self, card_data, reason="Manual block"):
        """
        Add card to blacklist.
        
        Args:
            card_data (str): Card data to block
            reason (str): Reason for blocking
        """
        card_hash = hashlib.sha256(card_data.encode()).hexdigest()
        
        if card_hash not in self.blacklist['blocked_cards']:
            self.blacklist['blocked_cards'].append({
                'hash': card_hash,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            })
            self._save_blacklist()
            return True
        return False
        
    def remove_from_blacklist(self, card_data):
        """
        Remove card from blacklist.
        
        Args:
            card_data (str): Card data to unblock
        """
        card_hash = hashlib.sha256(card_data.encode()).hexdigest()
        self.blacklist['blocked_cards'] = [
            item for item in self.blacklist['blocked_cards'] 
            if item.get('hash') != card_hash
        ]
        self._save_blacklist()
        
    def add_suspicious_pattern(self, pattern):
        """Add a new suspicious pattern to watch for."""
        if pattern not in self.blacklist['blocked_patterns']:
            self.blacklist['blocked_patterns'].append(pattern)
            self._save_blacklist()
            
    def get_blacklist(self):
        """Get current blacklist."""
        return self.blacklist
        
    def clear_blacklist(self):
        """Clear all blocked cards and patterns."""
        self.blacklist = {'blocked_cards': [], 'blocked_patterns': []}
        self._save_blacklist()
