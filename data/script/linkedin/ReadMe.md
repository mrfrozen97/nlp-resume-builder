# linkedin-job-scrape.py
- Implements the scrape_linkedin_url function to scrape a single job posting on linkedin.
- I have manually collected links for SDE intern job postings online and pass them through scrape_linkedin_url function and stored the data in a json file.
- To imitate the results for any other role, refer to the scrape_software_interns function.

# Steps to Use
1. Pull this code onto your local machine with ```git pull``
2. cd to the linkedin directory with ```cd data/script/linkedin```
3. Install prerequisites
    a. The ```requests``` package. You can install it via ```pip3 install requests```
    b. The ```beautiful soup``` package. You can install it via ```pip3 install beautifulsoup4```
4. Create a .txt file in the links folder
    a. This .txt file will have all the job links that will be scraped
5. Once the links are ready, create an empty json file. This will be where the data gets dumped.
    a. Ensure that this file is in proper JSON format. So once creating the file add empty curly braces to the empty file ```{}```
6. Finally, modify the ```linkedin-job-scrape.py``` to call the ```scrape_linked_url``` function with the appropriate parameters referring to your files. Then run the code with ```python3 linkedin-job-scrape.py```