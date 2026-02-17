# Monster Hunter Rise Mod Manager

A comprehensive GUI application for managing mods for Monster Hunter Rise, providing an easy way to install and uninstall various game enhancements.

## Features

The application provides a user-friendly graphical interface with features such as:

- Manage 15+ popular Monster Hunter Rise mods in one place
- Select all functionality for easy mod selection
- Custom loading splash screen
- Application icon for better identification
- Auto-detection of game installation path
- Game running detection to prevent installation conflicts
- Two executable options: single file or directory-based
- Automatic mod installation and uninstallation

This application manages a wide variety of Monster Hunter Rise mods:

### Core Framework
- **REFramework**: The core framework required for most mods
- **REFramework Direct2D**: Alternative Direct2D rendering for REFramework

### Gameplay Enhancement Mods
- **MHR Overlay**: A detailed in-game UI overlay that provides:
  - Damage Meter: Track damage dealt by all players in real-time
  - Monster Health Bars: Display health, stamina, and rage for large monsters
  - Buff Tracking: Monitor active buffs, debuffs, item effects, and melody effects
  - Endemic Life Information: Show details about environmental creatures
  - Player Stats: Display various player statistics
  - Time Display: Show quest time and other timing information
  - Small Monster Tracking: Information about small monsters in the area

- **Teleport Mod**: Teleportation functionality
- **Spirit Birds Mod**: Spirit Bird enhancements
- **Monster Weakness Icon Indicator**: Indicates the monster elemental weakness
- **Kill Cam (Currently unavailable)**: Adds slow motion on final hit and removes the monster kill cam cutscene sequences
- **Fast Return**: Skip carve timer and quest ending animation

### Quality of Life Mods
- **Drop Rates Enhanced Mod**: Enhanced drop rates with different balance options (Balanced, Not so Balanced, Unbalanced)
- **Auto Argosy Mod**: Automates the Argosy trading system
- **Auto Cohoot Nest Mod**: Automates gathering from Cohoot nests
- **Better Matchmaking**: Disables timeout when searching for Join Requests, removes region lock, and fixes language filter for lobbies

### Customization & Editor Mods
- **Charm Editor**: Edit charms (legal cheat only), all items cheat, and Zenny/Points editor
- **Custom In-Game Mod Menu**: User-friendly IMGUI-inspired API for drawing in-game settings menus for REFramework mods
- **Skip Intro Logo**: Skip logos and press any button to continue

## Installation

1. Download the latest release from the [Releases](https://github.com/jluo1996/MonsterHunterRise_Utilities/releases) page
2. Choose the appropriate executable for your needs:
   - **One-file executable** (.exe): A single executable file that runs directly (recommended for most users)
   - **One-directory executable** (.exe): An executable that extracts to a directory (useful if you need access to individual files)
3. Run the executable as administrator
4. The application will check if Monster Hunter Rise is currently running and prompt you to close it if necessary
5. When prompted, select the full path to your Monster Hunter Rise game installation directory (the app will attempt to auto-detect it)
6. Select the mods you want to install from the list
7. Click "Install Selected Mods"

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

Current version: 2.x.x.x - A comprehensive mod manager supporting 15+ popular Monster Hunter Rise mods

## Build & Distribution

This project uses GitHub Actions for automated builds and releases:
- **One-File Build**: Creates a single executable file for easy distribution
- **One-Directory Build**: Creates an executable with extracted files for modular access
- Automated version numbering based on build runs

## Credits

- Built with PyQt6 for the GUI framework
- Built using REFramework for mod support
- Special thanks to the Monster Hunter Rise modding community and all mod creators
- GitHub Actions for automated building and releases
