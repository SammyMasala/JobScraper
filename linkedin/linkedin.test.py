from scraperClass import LinkedInScraper


def runTest(scraper):
    # Test 1: Invalid URL returns a blank list
    URL_INVALID = "https://woops.com"
    assert scraper.getJobs(URL_INVALID) == [], "Invalid URL returns a blank list"

    # Test 2: Valid URL returns a list of URLs
    URL_VALID = "https://www.linkedin.com/jobs/search/?currentJobId=3764210435&geoId=101165590&keywords=" \
                 + "software" + "&location=" + "United%20Kingdom" \
                 + "&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true"
    result = scraper.getJobs(URL_VALID)
    assert len(result) > 0, "Valid URL returns a list of length > 0"
    assert "http" in result[0], "Results in list should be a URL"

    return "Test Success"


# Functional test: LinkedInScraper
scraperClass = LinkedInScraper()
print(runTest(scraperClass))
