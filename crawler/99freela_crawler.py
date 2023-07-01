import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

url = "https://www.99freelas.com.br/"

option = Options()
option.headless = True

driver = webdriver.Firefox()

driver.get(url)

# driver.maximize_window()

# Selecionando busca
search_element = driver.find_element("xpath",
                                     "//input[@placeholder='Buscar freelancers']")
search_element.send_keys("data science" + Keys.RETURN)

time.sleep(1)

page_size = 80

for page in range(page_size):
    # Clicar na aba
    if page < 21:
        page += 1
        el = f"//span[@data-page='{page}']"
        page = driver.find_element("xpath", el).click()
        continue
    try:
        page += 1
        el = f"//span[@data-page='{page}']"
        page = driver.find_element("xpath", el).click()
    except:
        continue

    time.sleep(2)

    # Pegando lista de freelas da página
    try:
        freelas_result = driver.find_element(By.CLASS_NAME, "result-list")
        html_content = freelas_result.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, "html.parser")
        ul_size = len(soup.find_all('li'))
    except:
        continue
    
    time.sleep(2)
    
    height = 500

    for user in range(ul_size):

        # Get freelas Name
        try:
            content = soup.find_all("li", {"class": "result-item"})
            name = content[user].find('img').get('title')
            name = str(name).strip()

            freela = driver.find_element(By.LINK_TEXT, name)
            
            if name == None: continue
            
            time.sleep(1)

            freela.click()
        
            time.sleep(1)
        
            freela_content = driver.find_element(By.CLASS_NAME, "box-profile-view")
            freela_content = freela_content.get_attribute('outerHTML')

            try:
                freela_soup = BeautifulSoup(freela_content, "html.parser")
                skills = freela_soup.find("div", {"class": "container-habilidades"})
                skills = skills.find_all("li", {"class": "tag-info"})
                skills = [skills[i].string for i in range(len(skills))]
            except: continue
            
            if skills == None: continue
            
            try:
                interest_areas = freela_soup.find("div", {"class": "container-areasdeinteresse"})
                interest = interest_areas.find_all("li", {"class": "tag-info"})
                interest = [interest[i].string for i in range(len(interest))]
            except: continue
            
            if interest == None: continue
        
            df = pd.read_csv("99freelas_dataScience.csv")
            df.loc[df.shape[0]] = [name, skills, interest]
            df.to_csv("99freelas_dataScience.csv", index=False)
        
            driver.back()   
            time.sleep(3)     
            driver.execute_script(f"window.scrollTo(0, {height})") 
            height += 250
        except:
            continue
        
        time.sleep(3)
        
    print(page)


time.sleep(2)
driver.quit()