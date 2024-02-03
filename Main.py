# Importing Required Packages
from selenium import webdriver
from bs4 import BeautifulSoup
import time, requests, gspread
from oauth2client.service_account import ServiceAccountCredentials

# Base URl of Linkedin Public Page
base_url = "https://www.linkedin.com/jobs/"
# Specific search criteria for fetching info
params = "search?keywords=&location=Cayman%20Islands&geoId=101679506&trk=public_jobs_jobs-search-bar_search-submit"
# Main URl to get Jons from
url = base_url + params
print(url)

# Initiating the driver (Chrome) but browser will not opened but it should be installed
headless_mode = webdriver.ChromeOptions()
headless_mode.add_argument('headless')
driver = webdriver.Chrome(options=headless_mode)

# Opening the URl in Browser but it will not be visible
driver.get(url)
print("URL opened Successfully")

# Storing the scrolling page value from last scrolled
last_scrolled_to = driver.execute_script("return document.body.scrollHeight")
# Running this code to scroll till the end of the page to get all info in the page as it is a lazyloading page
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    scrolled_to = driver.execute_script("return document.body.scrollHeight")
    if scrolled_to == last_scrolled_to:
        break
    last_scrolled_to = scrolled_to
print("Page scrolled successfully till last")

# Initiating BeautifulSoup to extract info from the fully loaded page
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
driver.quit()

# Storing Job ID
my_Job_ID = [job['data-row'] for job in soup.find_all("div", class_="base-card") if 'data-row' in job.attrs]
print(f"Extracted {len(my_Job_ID)} Job ID's successfully")

my_Tracking_ID = [job.get('data-tracking-id') for job in soup.find_all("div", class_="base-card") if 'data-tracking-id' in job.attrs]
print(f"Extracted {len(my_Tracking_ID)} Job Tracking ID's successfully")

# Storing Posted Date
my_posted_date = [job.find("time", class_="job-search-card__listdate")['datetime'] if "None" not in str(type(job.find("time", class_="job-search-card__listdate"))) else job.find("time", class_="job-search-card__listdate--new")['datetime'] for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_posted_date)} Posted dates successfully")

# Storing Months
my_Job_Posted_Month = [job[6:8] for job in my_posted_date]

# Storing Year
my_Job_Posted_Year = [job[:5] for job in my_posted_date]

# Storing all titles
my_titles = [job.find("span", class_="sr-only").text.strip() for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_titles)} Titles successfully")

# Storing Companies
my_companies = [job.find("h4", class_="base-search-card__subtitle").text.strip() for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_companies)} Companies successfully")

# Storing Locations
my_locations = [job.find("span", class_="job-search-card__location").text.strip() for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_locations)} Locations successfully")

# Storing Listed Date
my_listed_date = [job.find("time", class_="job-search-card__listdate").text.strip() if "None" not in str(type(job.find("time", class_="job-search-card__listdate"))) else job.find("time", class_="job-search-card__listdate--new").text.strip() for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_listed_date)} Listed dates successfully")

# Storing JOB URL
my_Job_URL = [job.find("a", class_="base-card__full-link", href=True)['href'] for job in soup.find_all(
    "div", class_="base-search-card")]
print(f"Extracted {len(my_Job_URL)} JOB URL's successfully")

# Storing Description
my_description = {}
my_Job_industry = []

try:
    for job in range(len(my_Job_URL)):
        page = requests.get(my_Job_URL[job])
        cat_sub_headings = []
        cat_text = []
        if page.status_code != 200:
            count = 0
            while page.status_code != 200:
                page = requests.get(my_Job_URL[job])
                soup = BeautifulSoup(page.content, "html.parser")
                my_description.update(
                    {job: soup.find("div", class_="show-more-less-html__markup").text.strip() if "None" not in str(type(soup.find("div", class_="show-more-less-html__markup"))) else " "})
                cat_sub_headings = [job.find(
                    "h3",  class_="description__job-criteria-subheader").text.strip() if "None" not in str(type(soup.findAll("h3",  class_="description__job-criteria-subheader"))) else " " for job in soup.findAll(
                    "li",  class_="description__job-criteria-item")]
                cat_text = [job.find(
                    "span",  class_="description__job-criteria-text--criteria").text.strip() if "None" not in str(type(soup.findAll("span",  class_="description__job-criteria-text--criteria"))) else " " for job in soup.findAll(
                    "li",  class_="description__job-criteria-item")]
                if job >= len(my_Job_industry):
                    my_Job_industry.append(
                        tuple(zip(cat_sub_headings, cat_text)))
                else:
                    my_Job_industry[job] = tuple(
                        zip(cat_sub_headings, cat_text))
                count += 1
                if count >= 15 and ("None" in str(type(soup.find("div", class_="show-more-less-html__markup")))):
                    headless_mode = webdriver.ChromeOptions()
                    headless_mode.add_argument('headless')
                    driver = webdriver.Chrome(options=headless_mode)
                    driver.get(my_Job_URL[job])
                    time.sleep(2)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    my_description.update(
                        {job: soup.find("div", class_="show-more-less-html__markup").text.strip() if "None" not in str(type(soup.find("div", class_="show-more-less-html__markup"))) else " "})
                    cat_sub_headings = [job.find(
                        "h3",  class_="description__job-criteria-subheader").text.strip() if "None" not in str(type(soup.findAll("h3",  class_="description__job-criteria-subheader"))) else " " for job in soup.findAll(
                        "li",  class_="description__job-criteria-item")]
                    cat_text = [job.find(
                        "span",  class_="description__job-criteria-text--criteria").text.strip() if "None" not in str(type(soup.findAll("span",  class_="description__job-criteria-text--criteria"))) else " " for job in soup.findAll(
                        "li",  class_="description__job-criteria-item")]
                    if job >= len(my_Job_industry):
                        my_Job_industry.append(tuple(zip(cat_sub_headings, cat_text)))
                    else:
                        my_Job_industry[job] = tuple(
                            zip(cat_sub_headings, cat_text))
                    driver.quit()
                    if (my_description[job] != " ") or count > 18:
                        break
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            my_description.update(
                {job: soup.find("div", class_="show-more-less-html__markup").text.strip() if "None" not in str(type(soup.find("div", class_="show-more-less-html__markup"))) else " "})
            cat_sub_headings = [job.find(
                "h3",  class_="description__job-criteria-subheader").text.strip() if "None" not in str(type(soup.findAll("h3",  class_="description__job-criteria-subheader"))) else " " for job in soup.findAll(
                "li",  class_="description__job-criteria-item")]
            cat_text = [job.find(
                "span",  class_="description__job-criteria-text--criteria").text.strip() if "None" not in str(type(soup.findAll("span",  class_="description__job-criteria-text--criteria"))) else " " for job in soup.findAll(
                "li",  class_="description__job-criteria-item")]
            if job >= len(my_Job_industry):
                my_Job_industry.append(
                    tuple(zip(cat_sub_headings, cat_text)))
            else:
                my_Job_industry[job] = tuple(
                    zip(cat_sub_headings, cat_text))
        if my_description[job] == " " :
            print("Something went wrong and we found empty Description for Job ID :", my_Job_ID[job])

    print(f"Extracted ({len(my_description)}, {len(my_Job_industry)}) Descriptions and Miscelleneous details Successfully respectively")
except Exception as e:
    print("Something went wrong whule extracting Description and some Miscelleneous Info :", e)

data = {}

key_val = 0

for job in range(len(my_titles)):
    data.update({job: {
        "JobID": my_Job_ID[job],
        "ID": my_Tracking_ID[job],
        "name": my_titles[job],
        "hiring_company": my_companies[job],
        "posted_time_friendly": my_listed_date[job],
        "snippet": my_description[job],
        "location": my_locations[job],
        "posted_time": my_posted_date[job],
        "source": "Linkedin",
        "theurl": my_Job_URL[job],
        "themonth": my_Job_Posted_Month[job],
        "theyear":my_Job_Posted_Year[job]
    }})
    for job_cat in my_Job_industry[job]:
        data[job].update({job_cat[0]:job_cat[1]})
    if len(list(data[job].keys())) >= key_val:
        key_val = len(list(data[job].keys()))

print(f"Converted {len(data)} extracted data in DICT format")

all_rows = []

for job in range(len(data)):
    all_rows.append(list(data[job].values()))

# Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("JSON.json", scope)
client = gspread.authorize(creds)

# Open the worksheet
worksheet = client.open("Rifat Job Feed").worksheet("Rifat Job Feed")

if len(data) > 0:
    worksheet.clear()
    worksheet.append_row(list(data[key_val].keys()))
    worksheet.append_rows(all_rows)
    print("Data has been successfully updated to Google Sheets.")
else:
    print("No job listings found.")

# Get the Google Spreadsheet link
spreadsheet_link = worksheet.url
print("Google Spreadsheet Link:", spreadsheet_link)

# {
#   "type": "service_account",
#   "project_id": "linkedin-jobs-413209",
#   "private_key_id": "d05ae0f93004e73f8f6a64325c5af5bf5a80cfc4",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCIdRdBJtFc69VD\n6y/6qzQ5WY7hUXu1sUnTvA26CL/prqdS2VACqI02inckJ/dXRGNnSPqj60ERT5V6\nMV5OynN5qbroD3YxDc8JNm2CwDIH4a76Pn/5uOlZHoj+qYfAmNC3cbiqtlraNB2o\nydld96vTwJjPz52OBtMncE8+VGHULrWhq0684jp/af+ZxFX6FYgEppq7dprYY+aX\nJyjFq/b1V4MSBxvj1VK/vnyi/GAPSqzsonJqoOXT+LqBbey8wmR1AbRnuy5otykZ\ns30e9/g9HPr0aadGenW7agPWHP98hkyodqluiG+12L7vYc4wkzdbxx83zuL0m1Wq\nfjkmVfgZAgMBAAECggEADY3WiycoQUWU6mklsTgTjjrCFslkM1jyegXs4HSsCLHL\ndvmU7p6qtXyCzGRCjOLYc32WlR+crUktZ3TDPFT0Vrpa5rVadRGSZgTc/dF0vBRZ\nBWGd4+0lEzAVms4LaOsE7aPDHFnT+RFCJ5jdGW4CHZy80QTQo+HeVBreFCqHiRlx\ngjpGwd3YrDFSbd8cb5up9BB2KwfQ4PQ/bFuYBMxS7y0uYwdSM1kiZFuHReIDTY43\nChabKxK50Trci4AlmhgxmRd3NZ6/a0VegJXKNJNCKDilToEjspBO28yWVVUk5/MU\nUD1xq4GRvd+Gd2iEIBmcuq9cLpcZKoHcO3nDMyhknQKBgQC/BjvkwiciauoRGoBZ\nJLCHxLTgXOApkVbFlGcOcIlQ1tzcCScFuOLOiAl/p8+UKNnqnGjJU8P4AjfXtnMk\ngbAjtyUsVBVKoKz6ZWk7yK+pF0QlIoGXpdkoQYXz3uZp89eReDq7V9rRxLj72jcn\npoJM5tR17J4LQGfePWj6w3+EHwKBgQC231jGnPDEIV9pInX8On+CzAiou2Xg13pj\naKTLtEcqzIF8dmJF9kbGwE2JIuwmbso97gCkAKyTRCBg7HwHrjaQIT/KvojrAOnn\nlASd7DBD5RJPLKqw9HXHOcI14RR9+VAq8NLeBO7FRt7putJyf+4lKLecnpqFgGhR\nZct0VOE8xwKBgEKI/lWYlp7zVGHutCPYlrBDgKjhUKbJ28pn/VlXM0z3+eeePHxO\nwJklYwGWxsOZUwXXwtvVFF4PD7pP710Y2uwlv4noI55hxr5UkknjhePEmdTBZxgW\nCURvRiQCUIk5CK2/jd1xJWOJPNFkWW+zHJGCmSAV8ZqDrWoIQ8eMTp8LAoGBALNw\nADoScKTiYi5VJBQ0ij2bWrvF9bdjd7HnUhyXbmVueXfY6aDggJ4wv2PaooEroMKX\nsIU8LBnsdSDlquYWaW+PUHrt7oc5REp5EPasdMeKFCcgGvS7Sn4MDKa1jlf1tFYO\nK7qyeF+WpNAPAsRbBx/rDg9eCR0J3FJSYgpp5wCtAoGAGkjUEBKoB3bNGj3fAWtN\nwRSLPxmkKmDBf2Grcoldk8iqbMHCP4QEM9pQ4Z7dAkOFkObLsAZynO5KOh+10Zgm\nkbliEndN9+aHHyNehj1bhTjC/WWmEuuT92R28bZyuJzKHXwRddARDektARD8GmHg\nlgBN+lTwY7jQ7T7e/9AzFNI=\n-----END PRIVATE KEY-----\n",
#   "client_email": "jobscrapper@linkedin-jobs-413209.iam.gserviceaccount.com",
#   "client_id": "115814442066477511926",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jobscrapper%40linkedin-jobs-413209.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }

