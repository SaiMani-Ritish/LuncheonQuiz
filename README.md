# 🎓 Luncheon Quiz

A Streamlit quiz application for live university events, using Google Sheets as a simple database.

---

## 📋 Complete Setup Guide (Step-by-Step)

---

## Step 1: Create a Google Sheet

1. Open your browser and go to **[sheets.google.com](https://sheets.google.com)**

2. Click the **+ Blank** button to create a new spreadsheet

3. Name your spreadsheet by clicking "Untitled spreadsheet" at the top-left
   - Name it something like: `Luncheon Quiz Scores`

4. **Copy the Spreadsheet ID** from the URL bar:
   ```
   https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789/edit
                                          ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                          THIS IS YOUR SPREADSHEET_ID
   ```
   
5. **Save this ID** somewhere - you'll need it later!

---

## Step 2: Create a Google Cloud Project

1. Go to **[console.cloud.google.com](https://console.cloud.google.com/)**

2. Sign in with your Google account (same one that owns the spreadsheet)

3. At the top of the page, click the project dropdown (says "Select a project")

4. In the popup, click **"NEW PROJECT"** (top-right of the popup)

5. Fill in:
   - **Project name**: `luncheon-quiz` (or any name you like)
   - **Organization**: Leave as default
   
6. Click **"CREATE"**

7. Wait 10-20 seconds for the project to be created

8. Make sure your new project is selected in the top dropdown

---

## Step 3: Enable Google Sheets API

1. In Google Cloud Console, click the **hamburger menu (☰)** at top-left

2. Navigate to: **APIs & Services** → **Library**

3. In the search box, type: `Google Sheets API`

4. Click on **"Google Sheets API"** in the results

5. Click the big blue **"ENABLE"** button

6. Wait for it to enable (takes a few seconds)

---

## Step 4: Create a Service Account

1. Click the **hamburger menu (☰)** again

2. Navigate to: **APIs & Services** → **Credentials**

3. Click **"+ CREATE CREDENTIALS"** at the top

4. Select **"Service account"**

5. Fill in:
   - **Service account name**: `streamlit-quiz`
   - **Service account ID**: (auto-fills based on name)
   - **Description**: `Service account for Streamlit quiz app` (optional)

6. Click **"CREATE AND CONTINUE"**

7. **Skip** the "Grant this service account access" step - click **"CONTINUE"**

8. **Skip** the "Grant users access" step - click **"DONE"**

---

## Step 5: Download the JSON Key

1. You should now see your service account in the list. Click on it:
   ```
   streamlit-quiz@your-project.iam.gserviceaccount.com
   ```

2. Click the **"KEYS"** tab at the top

3. Click **"ADD KEY"** → **"Create new key"**

4. Select **"JSON"** format

5. Click **"CREATE"**

6. A JSON file will download to your computer - **keep this file safe!**
   - File will be named something like: `your-project-abc123.json`

7. **Copy the `client_email`** from the JSON file - it looks like:
   ```
   streamlit-quiz@your-project.iam.gserviceaccount.com
   ```

---

## Step 6: Share Google Sheet with Service Account

1. Go back to your **Google Sheet** (from Step 1)

2. Click the green **"Share"** button (top-right)

3. In the "Add people and groups" field, paste the **service account email**:
   ```
   streamlit-quiz@your-project.iam.gserviceaccount.com
   ```

4. Make sure it says **"Editor"** (not Viewer)

5. **Uncheck** "Notify people" (service accounts can't receive emails)

6. Click **"Share"**

7. If asked about sharing with non-Google accounts, click **"Share anyway"**

---

## Step 7: Push Code to GitHub

1. Open a terminal/PowerShell in your project folder

2. Initialize Git and push:
   ```bash
   git init
   git add .
   git commit -m "Luncheon Quiz app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/LuncheonQuiz.git
   git push -u origin main
   ```

   ⚠️ Replace `YOUR_USERNAME` with your actual GitHub username

3. If you don't have a GitHub repo yet:
   - Go to [github.com](https://github.com) → Click **"+"** → **"New repository"**
   - Name it `LuncheonQuiz`
   - Keep it **Public** (required for free Streamlit Cloud)
   - **Don't** add README or .gitignore (we already have them)
   - Click **"Create repository"**
   - Then run the commands above

---

## Step 8: Deploy to Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**

2. Click **"Sign in"** → Sign in with your **GitHub** account

3. Click **"New app"** button

4. Fill in:
   - **Repository**: Select `YOUR_USERNAME/LuncheonQuiz`
   - **Branch**: `main`
   - **Main file path**: `app.py`

5. **BEFORE clicking Deploy** → Click **"Advanced settings"**

---

## Step 9: Add Secrets to Streamlit Cloud

1. In Advanced settings, click on the **"Secrets"** section

2. Open the JSON key file you downloaded (in a text editor like Notepad)

3. Copy-paste this template into the Secrets box, then fill in your values:

```toml
SPREADSHEET_ID = "paste-your-spreadsheet-id-here"

[GOOGLE_SHEETS]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...(your full key)...\n-----END PRIVATE KEY-----\n"
client_email = "streamlit-quiz@your-project.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-quiz%40your-project.iam.gserviceaccount.com"
```

### How to fill in each field:

| Field | Where to find it |
|-------|------------------|
| `SPREADSHEET_ID` | From the Google Sheet URL (Step 1) |
| `project_id` | In your JSON file: `"project_id": "..."` |
| `private_key_id` | In your JSON file: `"private_key_id": "..."` |
| `private_key` | In your JSON file: `"private_key": "..."` - Copy the ENTIRE key including `-----BEGIN...` and `-----END...` |
| `client_email` | In your JSON file: `"client_email": "..."` |
| `client_id` | In your JSON file: `"client_id": "..."` |
| `auth_uri` | Copy exactly as shown above |
| `token_uri` | Copy exactly as shown above |
| `auth_provider_x509_cert_url` | Copy exactly as shown above |
| `client_x509_cert_url` | In your JSON file: `"client_x509_cert_url": "..."` |

⚠️ **Important**: The `private_key` must be on ONE line with `\n` for newlines (it's already formatted this way in the JSON file)

---

## Step 10: Deploy!

1. Click **"Save"** to save secrets

2. Click **"Deploy!"**

3. Wait 1-2 minutes for the app to build

4. Your app will be live at:
   ```
   https://your-app-name.streamlit.app
   ```

5. **Test it!** Enter a name, complete the quiz, and check:
   - Your Google Sheet should have a new row with the score!

---

## 🎉 You're Done!

Share the app URL with your event participants and watch the leaderboard fill up!

---

## Managing Your Quiz

### View All Scores
Just open your Google Sheet - all scores appear there automatically!

### Reset for a New Event
1. Open your Google Sheet
2. Select all rows EXCEPT row 1 (the header)
3. Right-click → Delete rows
4. Done! Leaderboard is now empty

### Customize Questions
Edit `questions.py` in your repo, commit, and push. Streamlit Cloud will auto-redeploy.

---

## Troubleshooting

### "Google Sheets connection failed"
- ✅ Check SPREADSHEET_ID is correct (no extra spaces)
- ✅ Verify the sheet is shared with the service account email
- ✅ Make sure Google Sheets API is enabled
- ✅ Check private_key is complete (starts with `-----BEGIN` and ends with `-----END`)

### "Permission denied"
- The service account doesn't have Editor access to the sheet
- Go back to Step 6 and re-share with Editor permissions

### Scores not appearing in sheet
- Check the "scores" worksheet exists (app creates it automatically)
- Try refreshing the Google Sheet

---

## Project Files

```
LuncheonQuiz/
├── app.py              # Main quiz application
├── firebase.py         # Google Sheets integration
├── questions.py        # Quiz questions (edit to customize)
├── requirements.txt    # Python dependencies
├── .gitignore          # Prevents secrets from being committed
└── README.md           # This file
```

---

## License

MIT - Free to use for your events!
