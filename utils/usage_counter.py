import json
import os
from datetime import datetime
from pathlib import Path

class UsageCounter:
    """
    Tracks application usage count and statistics.
    Stores data persistently in a JSON file.
    """
    
    def __init__(self, data_file="usage_data.json"):
        self.data_dir = Path.home() / ".cardguard"
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / data_file
        self.data = self._load_data()
        
    def _load_data(self):
        """Load usage data from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading usage data: {e}")
                return self._initialize_data()
        else:
            return self._initialize_data()
            
    def _initialize_data(self):
        """Initialize new usage data structure."""
        return {
            'total_launches': 0,
            'first_launch': datetime.now().isoformat(),
            'last_launch': None,
            'launch_history': []
        }
        
    def _save_data(self):
        """Save usage data to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving usage data: {e}")
            
    def increment(self):
        """Increment usage counter."""
        self.data['total_launches'] += 1
        current_time = datetime.now().isoformat()
        self.data['last_launch'] = current_time
        self.data['launch_history'].append(current_time)
        
        # Keep only last 100 launches in history
        if len(self.data['launch_history']) > 100:
            self.data['launch_history'] = self.data['launch_history'][-100:]
            
        self._save_data()
        
    def get_count(self):
        """Get total launch count."""
        return self.data['total_launches']
        
    def get_statistics(self):
        """Get detailed usage statistics."""
        return {
            'total_launches': self.data['total_launches'],
            'first_launch': self.data['first_launch'],
            'last_launch': self.data['last_launch'],
            'recent_launches': len(self.data['launch_history'])
        }
        
    def reset(self):
        """Reset usage counter."""
        self.data = self._initialize_data()
        self._save_data()
