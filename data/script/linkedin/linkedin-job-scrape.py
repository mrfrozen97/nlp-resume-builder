import requests
from bs4 import BeautifulSoup
import json


# Classnames for field elements in the Linkedin job details html file
COMPANY_NAME = "topcard__org-name-link topcard__flavor--black-link"
JOB_TITLE = "sub-nav-cta__header"
JOB_DESCRIPTION = "show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"
JOB_LOCATION = "sub-nav-cta__meta-text"


# Function takes in a link and returns a dictionary/json of key value pairs of the data points
# prints data message if the data cannot be collected
def scrape_linkedin_url(link):
    try:
        data = {}
        req = requests.get(link)
        html_page = BeautifulSoup(req.text)
        # Using Bs4 parser to get elements containing data fields from the html file
        company_name = html_page.find("a", class_=COMPANY_NAME).text.lstrip().split("\n")[0]
        job_title = html_page.find("h3", class_=JOB_TITLE).text
        job_description = html_page.find("div", class_=JOB_DESCRIPTION).text.lstrip()
        job_location = html_page.find("span", class_=JOB_LOCATION).text

        data["id"] = link.split("/")[-1]
        data["Company"] = company_name
        data["title"] = job_title
        data["description"] = job_description
        data["location"] = job_location
        return data
    except:
        print("Error in retriving data")
        return None


# Run the scraper for all the links in the software_intern_links file
def scrape_software_interns():
    software_intern_links = open("software_intern_links", "r").read().split("\n")
    software_intern_data = json.load(open("software_intern_data.json", "r"))
    # Avoid duplicate data points by caching already scraped postings
    scraped_ids = {}
    for i in software_intern_data:
        if not isinstance(software_intern_data[i], str):
            scraped_ids[software_intern_data[i]['id']] = 0
    print(scraped_ids)
    index = len(scraped_ids)
    for i in software_intern_links:
        # Check if posting is already in the data
        if i.split("/")[-1] not in scraped_ids:
            print(i)
            temp_data = scrape_linkedin_url(i)
            if temp_data is not None:
                software_intern_data[index] = scrape_linkedin_url(i)
                index+=1
    json.dump(software_intern_data, open("software_intern_data.json", "w"), indent=2)


# Function to scrape software intern links
scrape_software_interns()
