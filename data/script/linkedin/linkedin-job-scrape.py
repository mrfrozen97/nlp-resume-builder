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
        id = link.split("/")[-1]
        if id == "" and len(link.split("/"))>1:
            id = link.split("/")[-2]
        data["id"] = id
        data["Company"] = company_name
        data["title"] = job_title
        data["description"] = job_description
        data["location"] = job_location
        return data
    except:
        print("Error in retriving data")
        return None


# Runs the scraper for all the links in the link_file
# Stores the data into a json data_file
def scrape_links_and_store_data(link_file, data_file):
    software_intern_links = open(link_file, "r").read().split("\n")
    software_intern_data = json.load(open(data_file, "r"))
    # Avoid duplicate data points by caching already scraped postings
    scraped_ids = {}
    for i in software_intern_data:
        if not isinstance(software_intern_data[i], str):
            scraped_ids[software_intern_data[i]['id']] = 0
    index = len(scraped_ids)
    for index, i in enumerate(software_intern_links):
        # Check if posting is already in the data
        id = i.split("/")[-1]
        if id == "" and len(i.split("/"))>1:
            id = i.split("/")[-2]
        if id not in scraped_ids:
            print(i, index)
            temp_data = scrape_linkedin_url(i)
            if temp_data is not None:
                software_intern_data[index] = scrape_linkedin_url(i)
                index+=1
    json.dump(software_intern_data, open(data_file, "w"), indent=2)



# Function to scrape software intern links
scrape_links_and_store_data("links/software_intern_links", "data/software_intern_data.json")


# Function to scrape Data Engineer links
scrape_links_and_store_data("links/data_engineering_links.txt", "data/data_engineering_data.json")

# Function to scrape Software Engineer links
scrape_links_and_store_data("links/software_engineer_links.txt", "data/software_engineer_data.json")

# Function to scrape DevOps links
scrape_links_and_store_data("links/devops_links.txt", "data/devops_data.json")

# Function to scrape CyberSecurity links
scrape_links_and_store_data("links/cybersecurity_engineer.txt", "data/cybersecurity_data.json")

# Function to scrape Cloud Infra links
scrape_links_and_store_data("links/cloud_infra_engineer.txt", "data/cloud_infra_data.json")

# Function to scrape Data Science links
scrape_links_and_store_data("links/data_science_links.txt", "data/data_science_data.json")

# Function to scrape AI ML links
scrape_links_and_store_data("links/al_ml_engineer.txt", "data/al_ml_data.json")
