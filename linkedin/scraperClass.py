import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LinkedInScraper:
    # CHANGE!! Returns links to all jobs
    def getJobs(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(0.5)
        return self.createJobList(self.maximizeJobPage(driver, 200))

    @staticmethod
    def maximizeJobPage(driver, numLoops):
        while numLoops > 0:
            try:
                page = driver.find_element(By.TAG_NAME, "body")
                page.send_keys(Keys.PAGE_DOWN)
                if numLoops % 5 == 0:
                    page.send_keys(Keys.PAGE_UP)
                # Click "See More" button
                seeMore = page.find_elements(By.CLASS_NAME, "infinite-scroller__show-more-button--visible")
                if seeMore:
                    seeMore[0].click()
                numLoops -= 1
            except Exception as exc:
                print(exc)
                break

        page = BeautifulSoup(driver.page_source, "html.parser")
        return page

    @staticmethod
    def createJobList(page):
        job_list = []

        for li in page.find_all('a', href=True):
            if '/jobs/' in li['href']:
                job_list.append(li['href'])

        return job_list
