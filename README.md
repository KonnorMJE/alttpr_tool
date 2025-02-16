# ALttPR Tool

A Python-based application designed to automate and enhance the process of setting up ALTTPR (A Link to the Past Randomizer) seeds.

## Features

- **MSU Audio Track Management**: Download and select MSU audio packs
- **Seed Generation**: Generate new game seeds with various presets
- **API Integration**: Utilizes pyz3r library for alttpr.com interactions
- **Google Integration**: Access Google Drive & Sheets for MSU pack management from the ALTTPR MSU Sheet

## Installation

### Windows
1. Download the latest release from the [Releases](https://github.com/KonnorMJE/alttpr_tool_2/releases) page
2. Extract the zip file
3. Run `alttpr_tool.exe`

Note: Windows may show a security warning. This is a false positive due to the Python-based executable. Click "More Info" → "Run Anyway" to proceed.

### MacOS/Linux Users
- Install UNRAR for archive extraction support
- (Additional installation steps to be added)

## First-Time Setup

1. On first launch, the program will create:
   - `errors.log` for logging
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
- MacOS/Linux: UNRAR

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements
Special thanks to:
- [@tcprescott](https://github.com/tcprescott) (Synack on Discord) for the pyz3r repository
- The sahasrahbot repository for preset files

## Contact
- Email: konnormje@gmail.com

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Google API Setup
For MSU downloading functionality, you'll need to set up Google API access. See [Google API Setup Guide](docs/GOOGLE_SETUP.md) for detailed instructions.