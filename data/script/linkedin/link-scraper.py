from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

# --- Your LinkedIn credentials ---
LINKEDIN_EMAIL = "your_email"
LINKEDIN_PASSWORD = "your_password"
SEARCH_TERM = "DevOPS"
PATH = "links/devops_links.txt"
# ----------------------------------

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)

def go_to_jobs_page(driver):
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(3)

    try:
        job_icon = driver.find_element(By.XPATH, '//li-icon[@type="job"]/ancestor::a')
        job_icon.click()
        time.sleep(3)
    except Exception as e:
        print("Failed to find or click the Jobs icon:", e)

def search_jobs(driver, keyword):
    try:
        search_input = driver.find_element(By.XPATH, '//input[@aria-label="Search by title, skill, or company"]')
        search_input.clear()
        search_input.send_keys(keyword)
        time.sleep(1)
        search_input.send_keys(Keys.RETURN)
        time.sleep(4)
    except Exception as e:
        print("Failed to search for jobs:", e)



def collect_job_links_with_pagination(driver, max_links=200, output_file="job_links.txt"):
    job_links_counter = 0
    page = 1
    
    with open(output_file, "w") as f:
        while job_links_counter < max_links:
            print(f"\nScraping page {page}...")
            time.sleep(2)

            jobs = driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
            print(f"Found {len(jobs)} job cards on page {page}")

            for job in jobs:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", job)
                    job.click()
                    time.sleep(2.5)

                    try:
                        job_link_element = driver.find_element(By.XPATH, '//a[contains(@href, "/jobs/view/")]')
                        href = job_link_element.get_attribute("href")
                        
                        if href and "/jobs/view/" in href:
                            f.write(f"{href}\n")
                            f.flush() 
                            job_links_counter += 1
                    except NoSuchElementException:
                        current_url = driver.current_url
                        if "/jobs/view/" in current_url:
                            f.write(f"{current_url}\n")
                            f.flush() 
                            job_links_counter += 1
                        else:
                            print("Could not find job link for this job")

                    if job_links_counter >= max_links:
                        print(f"Reached max links: {job_links_counter}")
                        return job_links_counter

                except (NoSuchElementException, ElementClickInterceptedException) as e:
                    print(f"Error clicking job: {e}")
                    continue

            try:
                next_page_btn = driver.find_element(By.XPATH, f'//li[@data-test-pagination-page-btn="{page + 1}"]')
                if next_page_btn.is_enabled():
                    next_page_btn.click()
                    page += 1
                    time.sleep(3)
                else:
                    print("No more pages to navigate.")
                    break
            except NoSuchElementException:
                print("⚠️ Pagination element not found. Ending pagination.")
                break

    print(f"\nCollected {job_links_counter} job links in total.")

def main():
    driver = setup_driver()
    linkedin_login(driver)
    go_to_jobs_page(driver)
    search_jobs(driver, SEARCH_TERM)
    collect_job_links_with_pagination(driver, max_links=200, output_file=PATH)
    input("Search complete. Press Enter to quit...")
    driver.quit()

if __name__ == "__main__":
    main()
