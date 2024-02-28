import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class IndeedScraper:
    # CHANGE!! Returns links to all jobs
    def getJobs(self, url, searchMax):
        job_list = []

        # To add: Loop to change page
        try:
            urlFront = url[:url.find("start=")+6]
            urlBack = url[url.find("start=")+7:]

            searchRange = 0
            while searchRange < searchMax:
                options = Options()
                options.add_argument("--disable-extensions")
                driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(3)
                driver.get(urlFront + str(searchRange) + urlBack)

                # Annoying Popups
                popup_annoying_cookies = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
                if popup_annoying_cookies:
                    popup_annoying_cookies[0].click()

                job_list += self.createJobList(driver.find_element(By.TAG_NAME, "body"))
                searchRange += 10
        except Exception as exc:
            print(exc)
        finally:
            return job_list

    @staticmethod
    def createJobList(page):
        job_list = []
        entries = page.find_elements(By.CLASS_NAME, "css-5lfssm")
        for entry in entries:
            new_job = []
            if entry.find_elements(By.TAG_NAME, "li"):
                # Append Job Link
                new_job.append(entry.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))

                page.send_keys(Keys.END)
                page.send_keys(Keys.PAGE_DOWN)
                entry.click()

                # Append Description
                new_job.append(page.find_elements(By.ID, "jobDescriptionText")[0].text)

                time.sleep(0.5)
                job_list.append(new_job)
        return job_list
