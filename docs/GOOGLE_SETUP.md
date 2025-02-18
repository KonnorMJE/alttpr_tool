# Setting up Google Access for ALTTPR Tool

**Time Estimate**: 10-15 minutes

📺 **[Video Guide Available Here](https://youtu.be/YN18TCOHGAM)** (Slightly out of date)

## Why is this needed?
ALTTPR Tool needs permission to read your Google Sheets data. This setup process is required by Google to ensure your data remains secure.

## Quick Setup Guide

### 1. Create Project (2 min)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click "Select a project" → "New Project"
4. Name it "ALTTPR Tool" → "Create"

### 2. Enable APIs (2 min)
1. Click [Enable Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) → "Enable"
2. Click [Enable Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) → "Enable"

### 3. Configure Consent Screen (2 min)
1. Click [OAuth consent screen](https://console.cloud.google.com/auth/overview/create)
2. Fill in the required details:
   - App Name: `ALTTPR Tool`
   - User support email: *Your Gmail*
3. Select "External" as the User Type and click "Create"
4. For "Contact Information", set "Email addresses" to *Your Gmail*, and click "Next"
5. Check the "I agree to the Google API Services: User Data Policy" checkbox, and click "Create"

### 4. Create OAuth Client (2 min)
1. Click [Create OAuth Client](https://console.cloud.google.com/auth/clients/create)
2. Configure:
   - Application Type: `Desktop app`
   - Name: `ALTTPR Tool`
3. Click "Create"

### 5. Configure Data Access (2 min)
1. Click [Data Access](https://console.cloud.google.com/auth/scopes)
2. Click "Add or Remove Scopes"
3. Select the following scopes:
   - https://www.googleapis.com/auth/drive.readonly
   - https://www.googleapis.com/auth/spreadsheets.readonly
4. Click "Update"
5. Click "Save"

### 6. Create Test User (2 min)
1. Click [Audience](https://console.cloud.google.com/auth/audience)
2. Under "Test users", click "+ Add Users"
3. Enter: *Your Gmail*
4. Click "Save"

### 7. Create Credentials File and Authenticate (3 min)
1. Click [Clients](https://console.cloud.google.com/auth/clients)
2. Click on the "ALTTPR Tool" client
3. Under "Client secrets", click the "Download JSON" button
4. Move the downloaded file to the `alttpr_tool/_internal/data` folder
5. Rename the downloaded file to `credentials.json`
6. Launch the application
7. Authorize access with your Google account when prompted

## Troubleshooting
- **"App not verified" warning?** This is normal. Click "Advanced" → "Go to ALTTPR Tool (unsafe)"
- **Need help?** [Open an Issue](https://github.com/yourusername/alttpr_tool/issues)

> **Note**: The application will create a `token.pickle` file after successful authorization. This token handles future authentication.