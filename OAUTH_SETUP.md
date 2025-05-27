# Google OAuth Setup for ShortGPT

## Overview
ShortGPT requires Google OAuth credentials for certain features. This guide explains how to set up your own credentials.

## Prerequisites
- Google Cloud Platform account
- Access to Google Cloud Console

## Setup Steps

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

### 2. Enable Required APIs
1. Navigate to "APIs & Services" > "Library"
2. Enable the following APIs:
   - Google Drive API (if using Drive integration)
   - YouTube Data API v3 (if using YouTube features)

### 3. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Configure the consent screen if prompted
4. Choose "Desktop application" as the application type
5. Add `http://localhost` to authorized redirect URIs
6. Download the credentials JSON file

### 4. Configure ShortGPT
1. Copy the downloaded JSON file to your ShortGPT directory
2. Rename it to `client.json`
3. The file should have this structure:

```json
{
    "installed": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "your-project-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uris": ["http://localhost"]
    }
}
```

## Security Notes

⚠️ **Important**: Never commit `client.json` to version control!

- The file contains sensitive credentials
- It's already added to `.gitignore`
- Use `client.json.template` as a reference for the structure

## Troubleshooting

### Common Issues
1. **Invalid credentials**: Ensure the JSON structure matches the template
2. **API not enabled**: Check that required APIs are enabled in Google Cloud Console
3. **Redirect URI mismatch**: Ensure `http://localhost` is in your OAuth client's redirect URIs

### Getting Help
- Check Google Cloud Console for API quotas and limits
- Verify your OAuth consent screen is properly configured
- Ensure your project has the necessary APIs enabled

## Alternative Setup
If you don't need Google integration features, you can skip this setup. ShortGPT will work without OAuth credentials for basic video processing functionality. 