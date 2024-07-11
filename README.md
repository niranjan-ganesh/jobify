# Introduction
Job search is an intense time consuming process. Having been in the job search phase, I realized it took me a lot of my productive time to browse through various jobsites and I was envisioning a tool that would simplify the search for me.

The aim of this project is to develop an automated solution for scraping job listings from LinkedIn and other major job portals and storing the data in a Google Sheets spreadsheet. This facilitates easy access, management, and analysis of job postings data which can be used to further this project. The primary goal is to save time and effort for those who regularly track job opportunities.

# Project Basics
I'm using BeautifulSoup for parsing HTML because of its flexible library for web scraping. Then I have used the cloudscraper module to bypass potential blocking mechanisms on the website, which makes the scraping process more robust. The Google Sheets integration was made possible with the gspread library and the OAuth2 authentication with Google service account credentials ensures secure access. I chose Google Sheets so that I can access the data from anywhere and eventually I'm planning to push the code to Google Cloud from where I can schedule it to run in a set interval of time. Using a spreadsheet helps me store the job data effectively in an organized manner.

For now, the program takes the inputs - job_title and location_country from the user to scrape for jobs.

# Current Implementation and Fixes
The current phase of the project focuses on LinkedIn. However, there is an issue where city and country names are not appearing in the spreadsheet. I think this is due to the incorrect parsing of these fields in the HTML structure and I'm currently working on it. A newer version with these fixes should be made available soon.

# Future Work
In the next phase, I will expand the scraping capabilities to include Indeed and other major job sites which will provide a comprehensive dashboard that aggregates job listings from multiple sources, offering a broader perspective on job opportunities including comprehensive search and recommendation capability. This will be the true essence of this project that I'm aiming for.

# Link to Google Sheets
The integrated spreadsheet can be accessed here - https://docs.google.com/spreadsheets/d/1zR2oXilhddqF3oOE3v74NUgcE0BaGA6e9ElpsZ3nEUU/edit?usp=sharing.
