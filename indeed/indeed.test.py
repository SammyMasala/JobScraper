from scraperClass import IndeedScraper


def runTest(scraper):
    # Test 1: Invalid URL returns a blank list
    URL_INVALID = "https://woops.com"
    assert scraper.getJobs(URL_INVALID, 10) == [], "Invalid URL returns a blank list"

    # Test 2: Valid URL returns a list of [URLs, description]
    URL_VALID = "https://uk.indeed.com/jobs?q=web+visa&l=United+Kingdom&start=0&vjk=af532b572ecb0e8c"
    result = scraper.getJobs(URL_VALID, 10)
    assert len(result) > 0, "Valid URL returns a list of length > 0"
    print(result)
    assert ".com" in result[0][0], "Results in list[0] should be a URL"

    return "Test Success"


# Functional test: LinkedInScraper
scraperClass = IndeedScraper()
print(runTest(scraperClass))
