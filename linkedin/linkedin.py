from bs4 import BeautifulSoup
from selenium import webdriver
from scraperClass import LinkedInScraper

# FOR LINKEDIN.COM

# Step 1. Edit keywords in URL. Be aware of how the each job site structures their url. E.g. spaces etc
SITE_LOCATION = "United%20Kingdom"  # Location/Country
SITE_SEARCHFIELD = "software"  # Job Role

# Step 2. Set URL to be scraped
# OPTION 1: Create link template and fill it with SITE_LOCATION and SITE_SEARCHFIELD.
SITE_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3764210435&geoId=101165590&keywords="\
              + SITE_SEARCHFIELD + "&location=" + SITE_LOCATION \
           + "&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true"

# OR OPTION 2: Just Copypasta the whole link directly from your browser!
# SITE_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3764210435&geoId=101165590&keywords="\
#            + "software&location=United%20Kingdom" \
#            + "&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true"

# Step 3. List keywords to be found
SEARCH_QUERIES = {
    "sponsor",
    "sponsorship"
}


def printList(jobs, queryList):
    for job_url in jobs:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(job_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = ""
        company = ""
        location = ""
        description = ""

        # CHANGE!! Find tags for jobs
        try:
            title = soup.find("h3", class_="sub-nav-cta__header")
            if title:
                title.get_text().strip()
            company = soup.find("a", class_="sub-nav-cta__optional-url").get_text().strip()
            if company:
                company.get_text().strip()
            location = soup.find("span", class_="sub-nav-cta__meta-text").get_text().strip()
            if location:
                location.get_text().strip()
            description = soup.find("div", class_="show-more-less-html__markup").get_text().strip()
            if description:
                description.get_text().strip()
        except Exception as exc:
            print(exc)
            pass

        # KEEP!!
        print("Link: " + job_url)
        for query in queryList:
            if query in description:
                print(title + " (" + company + ")")
                print(description)
                print(location)
                break


scraper = LinkedInScraper()
JOB_LIST = scraper.getJobs(SITE_URL)
printList(JOB_LIST, SEARCH_QUERIES)
