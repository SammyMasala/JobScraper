import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from JobClass import JobClass

# Step 1. Edit keywords. Be aware of how the url displays spaces, dashes etc. E.g. LinkedIn uses "%20"
JOB_LOCATION = "United%20Kingdom" # Job Location
JOB_KEYWORDS = "software" # Job Search

QUERY_KEYWORDS = { # Query for job description
    "sponsor",
    "sponsorship"
}

# Step 0?2?. Create link template and fill it. Ideally you started with a manual search to deconstruct and tokenize. 
JOBPAGE_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3764210435&geoId=101165590&keywords=" + JOB_KEYWORDS + "&location=" + JOB_LOCATION + "&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true"

## KEEP!! - SHOULD NOT CHANGE BETWEEN DIFFERENT JOBSITES
## CHANGE!! - MODIFY TO FIT SPECIFIC JOBSITES 

def loadLinkedIn(url):
    #### KEEP!!     
    driver = webdriver.Chrome()
    driver.get(url)
    elem = driver.find_element(By.TAG_NAME, "body")
    print(driver.page_source)
    

    ########## CHANGE!! Method to repeatedly populate job result page          
    ## LinkedIn: Scrolling to end of page 200 times XD    
    value = 200
    while value > 0:
        try:
            elem.send_keys(Keys.PAGE_DOWN)

            # Click "See More" button
            seeMore = driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
            if seeMore:
                seeMore.click()

            time.sleep(0.5)
            value -= 1
        except Exception as exc:
            print(exc)
            pass
    ##########

    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup
    ####

def getJobListings(page):
    ######## CHANGE!! Get list of jobs 
    job_list = []

    for li in page.find_all('a', href=True):
        if '/jobs/' in li['href']:
            job_list.append(li['href'])

    return job_list
    ########


def getJobInfo(driver, job_url):
    #### KEEP!!
    driver.get(job_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = ""
    company = ""
    location = ""
    description = ""
    link = ""

    ######## CHANGE!! Find tags for jobs
    try:
        title = soup.find("h3", class_="sub-nav-cta__header").get_text().strip()
        company = soup.find("a", class_="sub-nav-cta__optional-url").get_text().strip()
        location = soup.find("span", class_="sub-nav-cta__meta-text").get_text().strip()
        description = soup.find("div", class_="show-more-less-html__markup").get_text().strip()
        link = job_url
    except Exception as exc:
        print(exc)
        pass
    ########

    newJob = JobClass(title,company,location,description,link)

    print("Link: " + job_url)

    for query in QUERY_KEYWORDS:
        if query in description:
            print(title + " (" + company + ")")
            print(description)
            print(location)
            break
    ####

jobpage = loadLinkedIn(JOBPAGE_URL)
jobs = getJobListings(jobpage)

for job in jobs:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    _driver = webdriver.Chrome(options=options)
    getJobInfo(_driver,job)


