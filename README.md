# Monster Hunter Rise Mod Manager

A comprehensive GUI application for managing mods for Monster Hunter Rise, providing an easy way to install and uninstall various game enhancements.

## Features

This application manages several popular Monster Hunter Rise mods:

- **MHR Overlay**: A detailed in-game UI overlay that provides:
  - Damage Meter: Track damage dealt by all players in real-time
  - Monster Health Bars: Display health, stamina, and rage for large monsters
  - Buff Tracking: Monitor active buffs, debuffs, item effects, and melody effects
  - Endemic Life Information: Show details about environmental creatures
  - Player Stats: Display various player statistics
  - Time Display: Show quest time and other timing information
  - Small Monster Tracking: Information about small monsters in the area

- **REFramework**: The core framework required for most mods
- **REFramework Direct2D**: Alternative Direct2D rendering for REFramework
- **Teleport Mod**: Teleportation functionality
- **Spirit Birds Mod**: Spirit Bird enhancements
- **Drop Rates Enhanced Mod**: Enhanced drop rates with different balance options

## Installation

1. Download the latest release from the [Releases](https://github.com/jluo1996/MonsterHunterRise_Utilities/releases) page
2. Extract the executable file (MHR_Utilities.exe or similar)
3. Run the executable as administrator
4. When prompted, select the full path to your Monster Hunter Rise game installation directory (e.g., `C:\Program Files (x86)\Steam\steamapps\common\MonsterHunterRise\`)
5. Select the mods you want to install from the list
6. Click "Install Selected Mods"

## Requirements

- Monster Hunter Rise (PC)
- Windows 10 or later
- Administrator privileges for installation

## Usage

After installation:

1. Launch the Mod Manager application
2. Ensure the game installation path is correct (the app will try to auto-detect it)
3. Check the boxes next to the mods you want to install
4. Click "Install Selected Mods"
5. Launch Monster Hunter Rise to use the mods

### MHR Overlay Customization

For the MHR Overlay mod specifically:

- **In-Game Menu**: Press the configured hotkey (default: Insert) to open the customization menu
- **Configuration Files**: Settings are saved in `MonsterHunterRise\reframework\data\MHR Overlay\configs\`
- **Language Support**: Available in English, German, Japanese, Korean, Russian, Chinese Simplified, and Chinese Traditional

### Key Features

- **Real-time Updates**: All UI elements update in real-time during hunts
- **Performance Optimized**: Configurable update rates and performance settings
- **Modular Design**: Enable/disable individual mods as needed
- **Easy Management**: Simple GUI for installing and uninstalling mods

## Configuration

The MHR Overlay includes extensive customization options accessible in-game by pressing the Insert key (configurable). You can:

- Toggle visibility of individual modules
- Adjust positions and sizes
- Change colors and fonts
- Configure performance settings
- Switch languages

## Troubleshooting

- Check the log files in the `LogFiles` folder for any errors
- Make sure you're running the game and mod manager as administrator if UAC is enabled
- Ensure REFramework is properly installed before installing overlay mods

## Uninstall

To uninstall mods:

1. Run the Mod Manager application
2. Select the mods you want to uninstall
3. Click "Uninstall Selected Mods"

Alternatively, you can manually remove the mod files from your Monster Hunter Rise directory.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and entertainment purposes.

## Version

Current version: 2.xxx.xxx.xxx (MHR Overlay v2.7.3)

## Credits

- Built using REFramework
- Special thanks to the Monster Hunter Rise modding community
- PyQt6 for the GUI framework
