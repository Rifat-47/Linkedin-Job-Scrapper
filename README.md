# LinkedIn Job Scraper

Scrapes job listings from LinkedIn's public jobs page and pushes the results into a Google Spreadsheet — no LinkedIn account required.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/Rifat-47)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rifat-ibn-taher/)

---

## How it works

LinkedIn keeps their public jobs page open so that search engines like Google can index job listings. This scraper takes advantage of that:

1. Opens the LinkedIn jobs search URL in a headless Chrome browser (invisible window)
2. Scrolls to the bottom to trigger lazy-loaded results
3. Parses job cards with BeautifulSoup
4. Visits each job URL to fetch the full description
5. Pushes all data into a Google Sheet

No login, no LinkedIn API key needed.

---

## What gets scraped

| Field | Description |
|---|---|
| Job ID | LinkedIn's internal job ID |
| Tracking ID | LinkedIn's tracking ID |
| Title | Job title |
| Company | Hiring company name |
| Location | Job location |
| Posted Date | Date the job was posted |
| Description | Full job description |
| Job URL | Direct link to the job posting |
| Seniority / Type | Employment type, seniority level, etc. |

---

## Prerequisites

- Python 3.10+
- Google Chrome installed
- A Google account (for Google Sheets)

---

## Setup — Step 1: Clone the project

```bash
git clone https://github.com/Rifat-47/Linkedin-Job-Scrapper.git
cd Linkedin-Job-Scrapper
```

---

## Setup — Step 2: Create a virtual environment

```bash
python -m venv venv
```

**Activate it:**

On Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

On Windows (Command Prompt):
```cmd
venv\Scripts\activate.bat
```

On Mac / Linux:
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

---

## Setup — Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---|---|
| `selenium` | Controls Chrome to load and scroll the page |
| `webdriver-manager` | Auto-downloads the correct ChromeDriver for your Chrome version |
| `beautifulsoup4` | Parses the HTML to extract job data |
| `requests` | Fetches individual job detail pages |
| `gspread` | Reads and writes to Google Sheets |
| `oauth2client` | Authenticates with Google APIs |

---

## Setup — Step 4: Google Cloud configuration

This is a one-time setup so the script can write to your Google Sheet.

### 4a. Enable the APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g. `linkedin-scraper`)
3. Go to **APIs & Services** → **Enable APIs and Services**
4. Search for **Google Sheets API** → Enable it
5. Search for **Google Drive API** → Enable it

### 4b. Create a Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Give it any name (e.g. `jobscrapper`) → click **Done**
4. Click the service account email that was just created
5. Go to the **Keys** tab → **Add Key** → **Create new key** → select **JSON**
6. A `.json` file will be downloaded to your computer

It looks like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "xxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "jobscrapper@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

7. Rename this file to `JSON.json` and place it in the project root folder (next to `Main.py`)

> **Keep this file private.** Never commit it to GitHub — it is already listed in `.gitignore`.

---

## Setup — Step 5: Google Sheets configuration

1. Open [Google Sheets](https://sheets.google.com) and create a blank spreadsheet
2. Set the spreadsheet title to **`Job Feed`**
3. Rename the default sheet tab (at the bottom) to **`Jobs`**
4. Click the **Share** button (top right)
5. Paste the `client_email` from your JSON file (e.g. `jobscrapper@your-project-id.iam.gserviceaccount.com`)
6. Set the permission to **Editor** and click **Send**

The script now has permission to write to your sheet.

> If you want to use a different spreadsheet name or tab name, update these lines in `Main.py`:
> ```python
> worksheet = client.open("Job Feed").worksheet("Jobs")
> ```

---

## Running the scraper

Make sure your virtual environment is active (you should see `(venv)` in your prompt).

### Basic usage — single location

```powershell
python Main.py --locations "Bangladesh" --keyword "SQA Engineer"
```

### Multiple locations at once

```powershell
python Main.py --locations "Bangladesh" "United States" "Remote" --keyword "Software Engineer"
```

### Test without uploading to Google Sheets

```powershell
python Main.py --locations "Bangladesh" --keyword "SQA Engineer" --no-sheets
```

### No keyword filter (all jobs in that location)

```powershell
python Main.py --locations "Cayman Islands"
```

### All options

```
python Main.py --help

options:
  --locations   One or more locations  (e.g. "Bangladesh" "India" "Remote")
  --keyword     Job title keyword      (e.g. "SQA Engineer", "Data Analyst")
  --geo-ids     Optional LinkedIn geoIds matching each location in order
  --no-sheets   Skip Google Sheets upload (print results count only)
```

### After it runs

The terminal will print a Google Sheets link at the end like this:

```
Uploaded 13 jobs to Google Sheets.
Spreadsheet: https://docs.google.com/spreadsheets/d/...
```

Copy that link and open it in your browser to see the data.

---

## Built-in locations

These locations are pre-configured with their LinkedIn geoIds for accurate results:

| Location | Supported |
|---|---|
| United States | Yes |
| United Kingdom | Yes |
| Canada | Yes |
| Australia | Yes |
| Germany | Yes |
| France | Yes |
| India | Yes |
| Singapore | Yes |
| Bangladesh | Yes |
| Remote | Yes |

For any other location, just pass the name — LinkedIn will resolve it:

```powershell
python Main.py --locations "Pakistan" --keyword "Python Developer"
```

---

## Deactivate the virtual environment

When you are done:

```bash
deactivate
```

To completely remove the virtual environment:

```powershell
Remove-Item -Recurse -Force .\venv
```

---

## Screenshots

![Screenshot 1](https://github.com/Rifat-47/Linkedin-Job-Scrapper/blob/main/screenshots/1.png)

![Screenshot 2](https://github.com/Rifat-47/Linkedin-Job-Scrapper/blob/main/screenshots/2.png)

---

## Author

[@Rifat-47](https://github.com/Rifat-47)
