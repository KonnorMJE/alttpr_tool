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

## MIT License
Copyright 2025 KonnorMJE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.