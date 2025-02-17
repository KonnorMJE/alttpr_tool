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
2. On the APIs & Services dashboard, click "+ ENABLE APIS AND SERVICES"
3. Under "Google Workspace", enable:
   - Google Drive API
   - Google Sheets API

## Step 3: Configure Consent Screen
1. In the left sidebar, click "OAuth consent screen"
2. Select "Get Started"
3. Fill in the required details:
   - App Name: `ALTTPR Tool`
   - User support email: *Your Gmail*
4. Select "External" as the User Type and click "Create"
5. For "Contact Information", set "Email addresses" to *Your Gmail*, and click "Next"
6. Check the "I agree to the Google API Services: User Data Policy" checkbox, and click "Create"

## Step 4: Create OAuth Client
1. Select "Create OAuth Client"
2. Configure:
   - Application Type: `Desktop app`
   - Name: `ALTTPR Tool`
3. Click "Create"

## Step 5: Configure Data Access
1. In the left sidebar, click "Data Access"
2. Click "Add or Remove Scopes"
3. Select the following scopes:
   - https://www.googleapis.com/auth/drive.readonly
   - https://www.googleapis.com/auth/spreadsheets.readonly
4. Click "Update"
5. Click "Save"

## Step 6: Create Test User
1. In the left sidebar, click "Audience"
2. Under "Test users", click "+ Add Users"
3. Enter: *Your Gmail*
4. Click "Save"

## Step 7: Create Credentials File and Authenticate
1. In the left sidebar, click "Clients"
2. Click on the "ALTTPR Tool" client
3. Under "Client secrets", click the "Download JSON" button
4. Move the downloaded file to the `alttpr_tool/_internal/data` folder
5. Rename the downloaded file to `credentials.json`
6. Launch the application
7. Authorize access with your Google account when prompted

> **Note**: The application will create a `token.pickle` file after successful authorization. This token handles future authentication.