import os
import sys
import json
import hashlib
import platform
import subprocess
from typing import List, Dict, Optional
from pathlib import Path

class AppLocker:
    """Core application locking functionality"""
    
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = Path.home() / '.cardguard'
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.cards_file = self.config_dir / 'cards.json'
        self.locked_apps_file = self.config_dir / 'locked_apps.json'
        
        self.config = self._load_config()
        self.registered_cards = self._load_cards()
        self.locked_apps = self._load_locked_apps()
        
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {'pin_enabled': False, 'pin_hash': None}
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_cards(self) -> Dict:
        """Load registered cards"""
        if self.cards_file.exists():
            with open(self.cards_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cards(self):
        """Save registered cards"""
        with open(self.cards_file, 'w') as f:
            json.dump(self.registered_cards, f, indent=2)
    
    def _load_locked_apps(self) -> List:
        """Load locked applications list"""
        if self.locked_apps_file.exists():
            with open(self.locked_apps_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_locked_apps(self):
        """Save locked applications list"""
        with open(self.locked_apps_file, 'w') as f:
            json.dump(self.locked_apps, f, indent=2)
    
    def register_card(self, card_id: str, card_name: str = None) -> bool:
        """Register a new card"""
        if card_id in self.registered_cards:
            return False
        
        self.registered_cards[card_id] = {
            'name': card_name or f'Card {len(self.registered_cards) + 1}',
            'registered_at': str(Path.home())
        }
        self._save_cards()
        return True
    
    def unregister_card(self, card_id: str) -> bool:
        """Unregister a card"""
        if card_id in self.registered_cards:
            del self.registered_cards[card_id]
            self._save_cards()
            return True
        return False
    
    def is_card_registered(self, card_id: str) -> bool:
        """Check if card is registered"""
        return card_id in self.registered_cards
    
    def set_pin(self, pin: str) -> bool:
        """Set PIN for additional security"""
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        self.config['pin_enabled'] = True
        self.config['pin_hash'] = pin_hash
        self._save_config()
        return True
    
    def verify_pin(self, pin: str) -> bool:
        """Verify entered PIN"""
        if not self.config.get('pin_enabled'):
            return True
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        return pin_hash == self.config.get('pin_hash')
    
    def disable_pin(self) -> bool:
        """Disable PIN protection"""
        self.config['pin_enabled'] = False
        self.config['pin_hash'] = None
        self._save_config()
        return True
    
    def get_installed_apps(self) -> List[Dict]:
        """Get list of installed applications (cross-platform)"""
        apps = []
        system = platform.system()
        
        if system == 'Windows':
            apps = self._get_windows_apps()
        elif system == 'Darwin':  # macOS
            apps = self._get_macos_apps()
        elif system == 'Linux':
            apps = self._get_linux_apps()
        
        return apps
    
    def _get_windows_apps(self) -> List[Dict]:
        """Get Windows applications"""
        apps = []
        # Common Windows app locations
        program_files = [
            Path('C:/Program Files'),
            Path('C:/Program Files (x86)'),
            Path.home() / 'AppData/Local/Programs'
        ]
        
        for folder in program_files:
            if folder.exists():
                for item in folder.iterdir():
                    if item.is_dir():
                        # Look for .exe files
                        for exe in item.rglob('*.exe'):
                            if exe.is_file():
                                apps.append({
                                    'name': exe.stem,
                                    'path': str(exe),
                                    'type': 'application'
                                })
                                break  # Only get first exe in each folder
        
        return apps[:50]  # Limit to 50 apps for performance
    
    def _get_macos_apps(self) -> List[Dict]:
        """Get macOS applications"""
        apps = []
        app_folders = [Path('/Applications'), Path.home() / 'Applications']
        
        for folder in app_folders:
            if folder.exists():
                for app in folder.glob('*.app'):
                    apps.append({
                        'name': app.stem,
                        'path': str(app),
                        'type': 'application'
                    })
        
        return apps
    
    def _get_linux_apps(self) -> List[Dict]:
        """Get Linux applications"""
        apps = []
        desktop_files = [
            Path('/usr/share/applications'),
            Path.home() / '.local/share/applications'
        ]
        
        for folder in desktop_files:
            if folder.exists():
                for desktop_file in folder.glob('*.desktop'):
                    try:
                        with open(desktop_file, 'r') as f:
                            content = f.read()
                            if 'Name=' in content:
                                name = [line.split('=')[1] for line in content.split('\n') if line.startswith('Name=')][0]
                                apps.append({
                                    'name': name.strip(),
                                    'path': str(desktop_file),
                                    'type': 'application'
                                })
                    except:
                        pass
        
        return apps
    
    def lock_app(self, app_path: str, app_name: str) -> bool:
        """Add application to locked list"""
        app_data = {'path': app_path, 'name': app_name}
        if app_data not in self.locked_apps:
            self.locked_apps.append(app_data)
            self._save_locked_apps()
            return True
        return False
    
    def unlock_app(self, app_path: str) -> bool:
        """Remove application from locked list"""
        for app in self.locked_apps:
            if app['path'] == app_path:
                self.locked_apps.remove(app)
                self._save_locked_apps()
                return True
        return False
    
    def is_app_locked(self, app_path: str) -> bool:
        """Check if application is locked"""
        return any(app['path'] == app_path for app in self.locked_apps)
    
    def verify_access(self, card_id: str, pin: str = None) -> bool:
        """Verify if access should be granted"""
        # Check card registration
        if not self.is_card_registered(card_id):
            return False
        
        # Check PIN if enabled
        if self.config.get('pin_enabled'):
            if pin is None:
                return False
            return self.verify_pin(pin)
        
        return True
    
    def get_locked_apps(self) -> List[Dict]:
        """Get list of locked applications"""
        return self.locked_apps.copy()
    
    def get_registered_cards(self) -> Dict:
        """Get all registered cards"""
        return self.registered_cards.copy()

        return self.registered_cards.copy()
    
    # Additional helper methods for UI compatibility
    
    def remove_card(self) -> bool:
        """Remove the first registered card (for UI compatibility)"""
        if self.registered_cards:
            first_card_id = list(self.registered_cards.keys())[0]
            return self.unregister_card(first_card_id)
        return False
    
    def verify_card(self, card_id: str) -> bool:
        """Verify if card is registered"""
        return self.is_card_registered(card_id)
    
    def has_pin(self) -> bool:
        """Check if PIN is enabled"""
        return self.config.get('pin_enabled', False)
    
    def lock_apps(self, app_names: List[str]) -> bool:
        """Lock multiple applications by name"""
        try:
            for app_name in app_names:
                # Find app path from name
                apps = self.get_installed_apps()
                for app in apps:
                    if isinstance(app, dict) and app.get('name') == app_name:
                        self.lock_app(app.get('path', ''), app_name)
                        break
            return True
        except Exception as e:
            print(f"Error locking apps: {e}")
            return False
    
    def unlock_all_apps(self) -> bool:
        """Unlock all locked applications"""
        try:
            self.locked_apps.clear()
            self._save_locked_apps()
            return True
        except Exception as e:
            print(f"Error unlocking apps: {e}")
            return False
