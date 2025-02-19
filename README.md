# ALttPR Tool

A Python-based application designed to automate and enhance the process of setting up ALTTPR (A Link to the Past Randomizer) seeds.

## Features

- **MSU Audio Track Management**: Download and select MSU audio packs
- **Seed Generation**: Generate new game seeds with various presets
- **API Integration**: Utilizes [pyz3r](https://github.com/tcprescott/pyz3r) library for alttpr.com interactions
- **Google Integration**: Access Google Drive & Sheets for MSU pack management from the ALTTPR MSU Sheet
- **Auto start your tracker**: Define the path to your tracker executable, and the application will automatically start it once you've selected your MSU.

## Installation

### Windows
1. Download the latest release from the [Releases](https://github.com/KonnorMJE/alttpr_tool_2/releases) page
2. Extract the zip file
3. Run `alttpr_tool.exe`

Note: Windows may show a security warning. This is a false positive due to the Python-based executable. Click "More Info" → "Run Anyway" to proceed.

### MacOS/Linux Users
- A non-windows executable is not yet available, but is in the works.

## First-Time Setup

1. On first launch, the program will create:
   - `log_file.log` for logging
   - `alttpr_tool.db` for application state
   - A "CHANGEME" folder for default paths
2. You'll need to authenticate with Google (use your provided Gmail account)

## Troubleshooting

### Logging
The application creates a `log_file.log` in the executable's directory. By default, logging is set to ERROR level.

To enable detailed logging:
1. Open `log_level.txt`
2. Change to `LOG_LEVEL = DEBUG`
3. Restart the application

### Common Issues
- For file path copying: Shift + Right Click → "Copy as Path"
- For auto-running .sfc files: Set your emulator as the default application

## Database
The database file is located in `_internal/database` if you need to manage or reset it.

## Dependencies
- Windows: 7zip (included)

## Acknowledgements
Special thanks to:
- [@tcprescott](https://github.com/tcprescott) (Synack on Discord) for the [pyz3r](https://github.com/tcprescott/pyz3r) and [sahasrahbot](https://github.com/tcprescott/sahasrahbot) repositories

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Google API Setup
To use MSU downloading features, you'll need Google API access. Starting with version 1.1.0, there are two ways to set this up:

### Option 1: Use the "Managed" version (Recommended)
1. Download the "Managed" release (includes`client_secrets.json` file)
2. Send your Gmail address to [konnormje@gmail.com](mailto:konnormje@gmail.com) to be added to the testing whitelist
   > Note: This whitelist requirement is temporary until the Google Cloud project exits testing mode
3. Run the application and follow the OAuth prompt

### Option 2: Create Your Own Google Cloud Project
1. Download the "Selfhosted" release (no `client_secrets.json` file)
2. Set up your own Google Cloud project and credentials
3. Follow the instructions in the [Google API Setup Guide](docs/GOOGLE_SETUP.md)