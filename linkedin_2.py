import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper
import certifi
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# Function to initialize Google Sheets client
def initialize_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        print("Credentials initialized successfully.")

        client = gspread.authorize(creds)
        print("Google Sheets client initialized successfully.")
        return client
    except Exception as e:
        print(f"Error initializing Google Sheets client: {e}")

# Function to add data to Google Sheets
def add_to_google_sheets(sheet, data):
    # Check if the sheet is empty to add headers
    if len(sheet.get_all_records()) == 0:
        headers = ["Date Scraped", "Title", "Date Posted", "Job URL", "Company", "City", "Country"]
        sheet.append_row(headers)
    sheet.append_rows(data)
    print("Jobs exported to Google Sheets successfully")

# Function to scrape LinkedIn job listings
def scrape_linkedin(job_title, country):
    try:
        scraper = cloudscraper.create_scraper()
        job_title = job_title.replace(' ', '%20')
        url = f'https://www.linkedin.com/jobs/search?keywords={job_title}&location={country}'

        job_list = []
        while True:
            response = scraper.get(url, verify=certifi.where())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for job_card in soup.find_all('div', class_='base-search-card'):
                job = {}
                job['date_scraped'] = datetime.now().strftime('%Y-%m-%d')
                job['title'] = job_card.find('h3', class_='base-search-card__title').text.strip() if job_card.find('h3', class_='base-search-card__title') else 'N/A'
                job['date_posted'] = job_card.find('time')['datetime'] if job_card.find('time') else 'N/A'
                job['job_url'] = job_card.find('a')['href'] if job_card.find('a') else 'N/A'

                company_info = job_card.find('h4', class_='base-search-card__subtitle')
                if company_info:
                    company_info = company_info.text.split('·')
                    job['company'] = company_info[0].strip() if len(company_info) > 0 else 'N/A'
                    job['city'] = company_info[1].strip() if len(company_info) > 1 else 'N/A'
                    job['country'] = company_info[2].strip() if len(company_info) > 2 else 'N/A'
                else:
                    job['company'] = 'N/A'
                    job['city'] = 'N/A'
                    job['country'] = 'N/A'

                job_list.append(job)

            next_button = soup.find('button', class_='artdeco-pagination__button--next')
            if not next_button:
                break

            url = 'https://www.linkedin.com' + next_button['href']
            time.sleep(2)

        return pd.DataFrame(job_list)

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    job_title = input("Enter the job title: ")
    country = input("Enter the country: ")

    linkedin_df = scrape_linkedin(job_title, country)

    if not linkedin_df.empty:
        client = initialize_gspread()
        if client:
            sheet = client.open("Jobs").sheet1
            add_to_google_sheets(sheet, linkedin_df.values.tolist())
            print("\nLinkedIn DataFrame")
            print(linkedin_df)
        else:
            print("Failed to initialize Google Sheets client.")
    else:
        print("No jobs found or an error occurred.")