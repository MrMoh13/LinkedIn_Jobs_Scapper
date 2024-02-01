import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.webdriver.support.wait import WebDriverWait
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# initializing the chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
ser = Service("C:\\Users\\Tnluser\\Downloads\\chromedriver.exe")
driver = webdriver.Chrome(service=ser, options=options)
wait = WebDriverWait(driver, 10, poll_frequency=2, ignored_exceptions=[Exception])

# logging into the system
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3811703837&f_JT=F%2CC&f_WT=2&geoId=102713980&location=Ind&position=1&pageNum=0")
driver.maximize_window()
# Create empty lists

company_name = []
job_title = []
Job_Location = []
Job_url = []
# getting the job list
job_list = wait.until(EC.presence_of_all_elements_located((
    By.XPATH, "/html/body/div[1]/div/main/section/ul//li")))

# Loop to scroll through all jobs
i = 2
while i <= int((len(job_list) + 200) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1

    try:
        send = driver.find_element(By.XPATH,"//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)
        time.sleep(3)

    except:
        pass
        time.sleep(5)

job_list = wait.until(EC.presence_of_all_elements_located((
    By.XPATH, "/html/body/div[1]/div/main/section/ul//li")))
# Find company name and append it to the blank list

try:
    for i in range(len(job_list)):
        company = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')[i].text
        company_name.append(company)
except IndexError:
    print("__")

# Find title name and append it to the blank list

try:
    for i in range(len(job_list)):
        title = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')[i].text
        job_title.append(title)

except IndexError:
    print("__")

# Find location and append it to the blank list

try:
    for i in range(len(job_list)):
        location = driver.find_elements(By.CLASS_NAME, 'job-search-card__location')[i].text
        Job_Location.append(location)

except IndexError:
    print("__")

# Find job links

jobs = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
for e in jobs:
    Job_url.append(e.get_attribute('href'))

# Create a DataFrame
data = {
    "Company Name": company_name,
    "Job Title": job_title,
    "Job Location": Job_Location,
    "Job Url": Job_url
}

print(len(company_name))
print(len(job_title))
print(len(Job_Location))
print(len(Job_url))
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

sheet_name = "LinkedIn_Job_Scrapper"
gc = gspread.service_account()  # Use your own credentials
sh = gc.open(sheet_name)
worksheet = sh.get_worksheet(0)

# Get existing data from the Google Sheet
existing_data = get_as_dataframe(worksheet, usecols=[0])

# Append new data to the existing data
updated_data = pd.concat([existing_data, df], ignore_index=True)

# Update the Google Sheet with the combined data
set_with_dataframe(worksheet, updated_data)
