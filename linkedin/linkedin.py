from bs4 import BeautifulSoup
from selenium import webdriver
from scraperClass import LinkedInScraper

# Step 1. Edit keywords. Be aware of how the url displays spaces, dashes etc. E.g. LinkedIn uses "%20"
location = "United%20Kingdom"
searchField = "software"

# Step 0?2?. Create link template and fill it. Ideally you started with a manual search to deconstruct and tokenize. 
joblistUrl = "https://www.linkedin.com/jobs/search/?currentJobId=3764210435&geoId=101165590&keywords="\
              + searchField + "&location=" + location + "&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true"

scraper = LinkedInScraper()
jobs = scraper.getJobs(joblistUrl)
queryList = {
    "sponsor",
    "sponsorship"
}

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
    link = job_url

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
