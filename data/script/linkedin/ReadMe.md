# link-scraper.py
- Implements multiple functions to scrape linkedin job urls into a .txt file for job description scraping

# Steps to use Linked Job Link Scraper
1. Pull this code onto your local machine with ```git pull```
2. cd to the linkedin directory with ```cd data/script/linkedin```
3. Install prerequisites
    - The chrome web browser must be installed on this machine
    - The ```selenium``` package. You can install it via ```pip3 install selenium```
4. Create a .txt file in the links folder
    - This .txt file will be where all the job links get dumped
5. Once ready configure the following information in the script
    - Your Linkedin Email
    - Your Linkedin Password
    - The search term
    - The destination text file path
6. After providing all necessary information. Run the script with python3 ```link-scrape.py```
### Note: Ensure that the machine does not sleep during the scrape, otherwise the process will be terminated. If needed, you can run the script in headless mode (without the chrome browser UI) by adding options.add_argument("--headless") in the driver set up function.

# linkedin-job-scrape.py
- Implements the scrape_linkedin_url function to scrape a single job posting on linkedin.
- I have manually collected links for SDE intern job postings online and pass them through scrape_linkedin_url function and stored the data in a json file.
- To imitate the results for any other role, refer to the scrape_software_interns function.

# Steps to use Linkedin Job Description Scraper
1. Pull this code onto your local machine with ```git pull``
2. cd to the linkedin directory with ```cd data/script/linkedin```
3. Install prerequisites
    - The ```requests``` package. You can install it via ```pip3 install requests```
    - The ```beautiful soup``` package. You can install it via ```pip3 install beautifulsoup4```
4. Create a .txt file in the links folder
    - This .txt file will have all the job links that will be scraped
5. Once the links are ready, create an empty json file. This will be where the data gets dumped.
    - Ensure that this file is in proper JSON format. So once creating the file add empty curly braces to the empty file ```{}```
6. Finally, modify the ```linkedin-job-scrape.py``` to call the ```scrape_linked_url``` function with the appropriate parameters referring to your files. Then run the code with ```python3 linkedin-job-scrape.py```