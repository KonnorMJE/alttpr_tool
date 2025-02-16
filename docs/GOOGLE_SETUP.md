# Setting up Google Drive/Sheets API for ALTTPR Tool

📺 **[Video Guide Available Here](https://youtu.be/YN18TCOHGAM)**

## Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click on "Select a project" at the top of the page (next to "Google Cloud")
4. In the popup, click on "New Project" in the top right corner
5. Name your project "ALTTPR Tool" and click "Create"

## Step 2: Enable Required APIs
1. From the landing screen, click on "APIs & Services"
2. On the APIs & Services dashboard, click "+ ENABLES APIS AND SERVICES"
3. Under "Google Workspace", enable:
   - Google Drive API
   - Google Sheets API

## Step 3: Configure Consent Screen
1. In the left sidebar, click "OAuth consent screen"
2. Select "External" as the User Type and click "Create"
3. Fill in the required details:
   - App Name: `ALTTPR Tool`
   - User support email: *Your Gmail*
   - Developer contact information: *Your Gmail*
4. Click "Save and Continue"
5. In the "Scopes" tab:
   - Click "Add or Remove Scopes"
   - Enter the following scopes:
     ```
     https://www.googleapis.com/auth/drive.readonly
     https://www.googleapis.com/auth/spreadsheets.readonly
     ```
   - Select both checkboxes and click "Update"
6. Click "Save and Continue"
7. In the "Test users" tab:
   - Click "+ Add Users"
   - Enter your Gmail
   - Click "Add"
8. Review the Summary page before proceeding

## Step 4: Create Credentials
1. In the left sidebar, click "Credentials"
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. Configure:
   - Application Type: `Desktop app`
   - Name: `ALTTPR Tool`
4. Click "Create"
5. Download the JSON file
6. Rename the downloaded file to `credentials`

## Step 5: Setup with ALTTPR Tool
1. Place `credentials` file in `alttpr_tool/_internal/data` folder
2. Launch the application
3. Authorize access with your Google account when prompted

> **Note**: The application will create a `token.pickle` file after successful authorization. This token handles future authentication.


