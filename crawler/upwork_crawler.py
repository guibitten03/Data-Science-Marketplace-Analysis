import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json


url = "https://www.upwork.com/nx/jobs/search/?from_recent_search=true&q=data%20science&sort=recency"

option = Options()
option.headless = True

driver = webdriver.Firefox()

driver.get(url)

NUM_PAGES = 500

time.sleep(3)

for page in range(NUM_PAGES):
    # Peguei a lista de trabalhos da pagina x
    section_element = driver.find_element("xpath",
        "//div[@data-test='job-tile-list']")
    list_content = section_element.get_attribute('outerHTML')
    soup = BeautifulSoup(list_content, "html.parser")
    keys = soup.find_all("section", {"class":"up-card-section"})
    keys = [keys[i].attrs['data-test-key'] for i in range(len(keys))]

    time.sleep(1)

    height = 400
    
    job_contents = []

    for job in range(len(keys)):
        # Peguei o trabalho y da lista de trabalhos x
        present_card = driver.find_element("xpath",
            f"//section[@data-test-key='{keys[job]}']").click()

        time.sleep(4)

        content = driver.find_element(By.CLASS_NAME, "cfe-ui-job-details-content")
        content = content.get_attribute('outerHTML')
        content = BeautifulSoup(content, "html.parser")
        job_contents.append(content)

        time.sleep(1)
        driver.back()   
        time.sleep(3) 
        driver.execute_script(f"window.scrollTo(0, {height})") 
        time.sleep(1)
        height += 250
        
    time.sleep(1)
    
    df = pd.read_csv("upwork_dataScience.csv")
    prev_col = list(df['content'].values)
    prev_col += job_contents
    new_df = pd.DataFrame({"content":prev_col})
    new_df.to_csv("upwork_dataScience.csv", index=False)
    del new_df
    
    driver.find_element(By.XPATH, 
            "//button[contains(@class, 'up-pagination-item up-btn up-btn-link')]//*[contains(., 'Next')]/..").click()
    
    time.sleep(3)
    

time.sleep(2)
driver.quit()