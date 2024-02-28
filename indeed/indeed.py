from bs4 import BeautifulSoup
from selenium import webdriver
from scraperClass import IndeedScraper

# FOR INDEED.COM

# Step 1. Edit keywords in URL. Be aware of how the each job site structures their url. E.g. spaces etc
SITE_LOCATION = "United+Kingdom"  # Location/Country
SITE_SEARCHFIELD = "junior+developer"  # Job Role

# Step 2. Set URL to be scraped
# OPTION 1: Create link template and fill it with SITE_LOCATION and SITE_SEARCHFIELD.
SITE_URL = "https://uk.indeed.com/jobs?q=" \
           + SITE_SEARCHFIELD + "&l=" + SITE_LOCATION + "&fromage=30&start=10&vjk=2dcf4ec1ea4167fb"

# OR OPTION 2: Just Copypasta the whole link directly from your browser!
# SITE_URL = "https://uk.indeed.com/jobs?q=web+visa&l=United+Kingdom&fromage=30&start=10&vjk=2dcf4ec1ea4167fb"

# Step 3. List keywords to be found
SEARCH_QUERIES_INCLUDE = {
    "javascript",
    "react.js",
    "sql",
    "html",
    # "sponsor",
    # "sponsorship",
    # "skilled worker"
}
SEARCH_QUERIES_EXCLUDE = {
    "right to work",
    "do not offer",
    "unable to sponsor",
    "will not sponsor",
    "without sponsorship",
    "eligible to work",
    "cannot sponsor",
    "do not sponsor",
    "does not sponsor",
    "will not sponsor",
    "does not provide sponsorship",
    "security clearance",
    "cannot provide sponsorship",
    "does not qualify",
    "not require sponsorship"
}

# Step 4: Number of pages to search. Format as number of pages*10
NUM_PAGES = 200


def printList(jobs, queryListInclude, queryListExclude):

    for job in jobs:
        passedQueries = False
        jobDescription = job[1]

        # INCLUDE
        for query in queryListInclude:
            if query in jobDescription.lower():
                passedQueries = True
                break

        # EXCLUDE
        for query in queryListExclude:
            if query in jobDescription.lower():
                passedQueries = False
                break

        if passedQueries:
            print(job[0])
            print(job[1])
            print("-----------------")


scraper = IndeedScraper()
JOB_LIST_RAW = scraper.getJobs(SITE_URL, NUM_PAGES)
JOB_LIST_NO_DUPLICATES = []
for jobUnfiltered in JOB_LIST_RAW:
    existsFlag = False
    for jobFiltered in JOB_LIST_NO_DUPLICATES:
        if jobUnfiltered[0] == jobFiltered[0]:
            existsFlag = True
            break
    if not existsFlag:
        JOB_LIST_NO_DUPLICATES.append(jobUnfiltered)
printList(JOB_LIST_NO_DUPLICATES, SEARCH_QUERIES_INCLUDE, SEARCH_QUERIES_EXCLUDE)
