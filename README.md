
# Project Title

Linkedin Job Scrapper.

Purpsoe: Linkedin Jobs are scrapped & updated on google spreadsheet. 

## Run Locally

Clone the project

```bash
  https://github.com/Rifat-47/Linkedin-Job-Scrapper.git
```

Go to the project directory

```bash
  cd Linkedin-Job-Scrapper
```

Install virtual environment

```bash
  pip install virtualenv
```

Create a virtual environment with name 'venvname'
```bash
  python -m venv venvname
```

Activate virtual environment
```bash
  venvname\Scripts\activate
```

Install dependencies
```bash
  pip install -r requirements.txt
```

Run the python script
```bash
  python Main.py
```

After running the script, google spreadsheet link will be printed in the terminal. Copy and paste the link in the browser. You will be able to view the data on spreadsheet. Right now, I have given view acess to anyone with the link.

Deactivate virtual environment (on windows command prompt/powetshell)
```bash
  deactivate
```
## Documentation

To remove virtual environment completely: 
```bash
  Remove-Item -Recurse -Force .\venvname
```

Project can be run without using virtual environment.
```bash
  https://github.com/Rifat-47/Linkedin-Job-Scrapper.git
  cd Linkedin-Job-Scrapper
  pip install -r packages.txt
  python Main.py 
```

But it is recommended to use virtual environment.

-------------------------------------------------

Let's discuss, how to get the get the api credentials and access the google spredsheet.

At first, let's fix the google cloud configuration.
1. go to "https://console.cloud.google.com/"
2. Create a New Project 
3. Go to Api & Services.
4. Click on "ENABLE APIS AND SRVICES" tab
5. Search "Goggle Sheets API" and Enable it.
6. Search "Google Drive API" ad Enable it.
7. Click on "Credentials" tab 
8. Click on "CRATE CREDENTIALS" and select Service Account 
9. Enter Service Account Name and click done.
10. Now, click on the email under Service Accounts section. Select "KEYS" tab > ADD Key > Create new key > select JSON.
A json file with below info will be downloaded in your pc.
```bash
  {
  "type": "service_account",
  "project_id": "linkedin-jobs-413209",
  "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCIdRdBJtFc69VD\n6y/6qzQ5WY7hUXu1sUnTvA26CL/prqdS2VACqI02inckJ/dXRGNnSPqj60ERT5V6\nMV5OynN5qbroD3YxDc8JNm2CwDIH4a76Pn/5uOlZHoj+qYfAmNC3cbiqtlraNB2o\nydld96vTwJjPz52OBtMncE8+VGHULrWhq0684jp/af+ZxFX6FYgEppq7dprYY+aX\nJyjFq/b1V4MSBxvj1VK/vnyi/GAPSqzsonJqoOXT+LqBbey8wmR1AbRnuy5otykZ\ns30e9/g9HPr0aadGenW7agPWHP98hkyodqluiG+12L7vYc4wkzdbxx83zuL0m1Wq\nfjkmVfgZAgMBAAECggEADY3WiycoQUWU6mklsTgTjjrCFslkM1jyegXs4HSsCLHL\ndvmU7p6qtXyCzGRCjOLYc32WlR+crUktZ3TDPFT0Vrpa5rVadRGSZgTc/dF0vBRZ\nBWGd4+0lEzAVms4LaOsE7aPDHFnT+RFCJ5jdGW4CHZy80QTQo+HeVBreFCqHiRlx\ngjpGwd3YrDFSbd8cb5up9BB2KwfQ4PQ/bFuYBMxS7y0uYwdSM1kiZFuHReIDTY43\nChabKxK50Trci4AlmhgxmRd3NZ6/a0VegJXKNJNCKDilToEjspBO28yWVVUk5/MU\nUD1xq4GRvd+Gd2iEIBmcuq9cLpcZKoHcO3nDMyhknQKBgQC/BjvkwiciauoRGoBZ\nJLCHxLTgXOApkVbFlGcOcIlQ1tzcCScFuOLOiAl/p8+UKNnqnGjJU8P4AjfXtnMk\ngbAjtyUsVBVKoKz6ZWk7yK+pF0QlIoGXpdkoQYXz3uZp89eReDq7V9rRxLj72jcn\npoJM5tR17J4LQGfePWj6w3+EHwKBgQC231jGnPDEIV9pInX8On+CzAiou2Xg13pj\naKTLtEcqzIF8dmJF9kbGwE2JIuwmbso97gCkAKyTRCBg7HwHrjaQIT/KvojrAOnn\nlASd7DBD5RJPLKqw9HXHOcI14RR9+VAq8NLeBO7FRt7putJyf+4lKLecnpqFgGhR\nZct0VOE8xwKBgEKI/lWYlp7zVGHutCPYlrBDgKjhUKbJ28pn/VlXM0z3+eeePHxO\nwJklYwGWxsOZUwXXwtvVFF4PD7pP710Y2uwlv4noI55hxr5UkknjhePEmdTBZxgW\nCURvRiQCUIk5CK2/jd1xJWOJPNFkWW+zHJGCmSAV8ZqDrWoIQ8eMTp8LAoGBALNw\nADoScKTiYi5VJBQ0ij2bWrvF9bdjd7HnUhyXbmVueXfY6aDggJ4wv2PaooEroMKX\nsIU8LBnsdSDlquYWaW+PUHrt7oc5REp5EPasdMeKFCcgGvS7Sn4MDKa1jlf1tFYO\nK7qyeF+WpNAPAsRbBx/rDg9eCR0J3FJSYgpp5wCtAoGAGkjUEBKoB3bNGj3fAWtN\nwRSLPxmkKmDBf2Grcoldk8iqbMHCP4QEM9pQ4Z7dAkOFkObLsAZynO5KOh+10Zgm\nkbliEndN9+aHHyNehj1bhTjC/WWmEuuT92R28bZyuJzKHXwRddARDektARD8GmHg\nlgBN+lTwY7jQ7T7e/9AzFNI=\n-----END PRIVATE KEY-----\n",
  "client_email": "jobscrapper@linkedin-jobs-413209.iam.gserviceaccount.com",
  "client_id": "115814442066477511926",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jobscrapper%40linkedin-jobs-413209.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```
Now, copy & paste the json file in the project directroy. Don't forget to change the json filename in the code.

-------------------------------------------------

Then, let's fix google spreadsheet configuration.
1. Create a blank spredsheet from Google Apps in your gmail account.
2. Change the spreadsheet title and the sheet name. In my case, title is "Job Feed" and sheet is named "Jobs". 
Any name can be given but make sure to change too in the code.
3. Now, share the google spreadsheet as editor with the client_email provided in the json file. 
In my case, it was: jobscrapper@linkedin-jobs-413209.iam.gserviceaccount.com

Finally, you are ready to go and run the python script. After running the script, google spreadsheet link will be printed in the terminal. Copy and paste the link in the browser & check if the spreadsheet is updated or not. 

You can check the screenshots, I have attached below.   

Fee free to reach out to me for any confusion. 
## Screenshots

![ScreenShot-1](https://github.com/Rifat-47/Linkedin-Job-Scrapper/blob/main/screenshots/1.png)

![ScreenShot-2](https://github.com/Rifat-47/Linkedin-Job-Scrapper/blob/main/screenshots/2.png)
## Authors

- [@Rifat-47](https://github.com/Rifat-47)


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/Rifat-47)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rifat-ibn-taher/)


