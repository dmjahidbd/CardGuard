# CardGuard

**Cross-platform card management application with hardware integration, usage tracking, and push notifications**

## Features

- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🔌 **Hardware Integration**: Connect and interact with card scanning devices
- 📊 **Usage Tracking**: Persistent usage statistics and launch history
- 🔒 **Security Features**: Block suspicious cards with pattern detection
- 🔔 **Push Notifications**: Real-time notifications for updates and security alerts
- 📝 **Activity Logging**: Detailed logs of all operations
- 🎨 **Modern UI**: Built with PyQt6 for a clean, responsive interface

## Project Structure

```
cardguard/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── ui/
│   └── main_window.py        # Main application window
│
├── utils/
│   ├── notifier.py           # Push notification system
│   ├── usage_counter.py      # Usage tracking
│   └── block_manager.py      # Security and blocking
│
└── hardware/
    └── device_handler.py     # Hardware device integration
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dmjahidbd/CardGuard.git
cd CardGuard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Connecting a Device

1. Launch CardGuard
2. Click "Connect Device" button
3. Wait for device connection confirmation
4. Device status will update to "Connected"

### Scanning Cards

1. Ensure device is connected
2. Click "Scan Card" button
3. Application will process card data
4. Results displayed with security check

### Security Features

CardGuard includes built-in security:

- **Suspicious Pattern Detection**: Automatically flags invalid or malformed card data
- **Blacklist Management**: Maintain a list of blocked cards
- **Block Toggle**: Enable/disable automatic blocking on suspicious activity

### Usage Statistics

- Total launches tracked automatically
- Launch history stored in `~/.cardguard/usage_data.json`
- Click "Refresh" to update statistics

## Configuration

### Data Storage

CardGuard stores data in your home directory:

- **Usage Data**: `~/.cardguard/usage_data.json`
- **Blacklist**: `~/.cardguard/blacklist.json`

### Notifications

Notifications are platform-specific:

- **Windows**: Console notifications (can be extended with win10toast)
- **macOS**: Native osascript notifications
- **Linux**: notify-send notifications

## Development

### Tech Stack

- **GUI Framework**: PyQt6
- **Language**: Python 3
- **Data Storage**: JSON files
- **Platform Detection**: platform module

### Module Overview

#### Main Application (`main.py`)
Entry point that initializes PyQt6 and launches the main window.

#### UI Module (`ui/main_window.py`)
Main window with:
- Device connection controls
- Card scanning interface
- Activity log viewer
- Security settings

#### Utility Modules (`utils/`)
- **notifier.py**: Cross-platform push notifications
- **usage_counter.py**: Tracks application launches and usage statistics
- **block_manager.py**: Manages security blacklist and suspicious pattern detection

#### Hardware Module (`hardware/device_handler.py`)
Handles device connectivity and card scanning (currently simulated for demo).

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Real hardware device integration
- [ ] Database storage (SQLite)
- [ ] User authentication
- [ ] Cloud sync capabilities
- [ ] Advanced reporting and analytics
- [ ] Multi-language support
- [ ] Custom icon support
- [ ] Update checking from remote server

## License

This project is open source and available under the MIT License.

## Author

**dmjahidbd**

- GitHub: [@dmjahidbd](https://github.com/dmjahidbd)

## Acknowledgments

- Built with PyQt6
- Inspired by modern card management systems
- Thanks to the open-source community

## Version

**Current Version**: 1.0.0

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
