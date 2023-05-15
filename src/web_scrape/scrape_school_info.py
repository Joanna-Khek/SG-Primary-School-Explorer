# Selenium Web Scraping
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from tqdm import tqdm
import time

def get_programme_details():
    try:
        driver.find_elements(By.CLASS_NAME, "moe-collapsible__heading")[1].click()
        time.sleep(1)
        programmes = driver.find_elements(By.CLASS_NAME, "moe-collapsible__content")[1].text
    except:
        programmes = ''
    return programmes

def get_cca_details():
    check_cca = driver.find_elements(By.XPATH, "//span[@class='moe-collapsible__heading'][contains(text(),'Co-Curricular Activities (CCAs)')]")
    if len(check_cca) == 1:
        driver.find_elements(By.CLASS_NAME, "moe-collapsible__heading")[2].click()
        time.sleep(1)
        cca = driver.find_elements(By.CLASS_NAME, "moe-collapsible__content")[2].text
    else:
        cca = ''
    return cca

def get_school_info():
    check_length = driver.find_elements(By.XPATH, '//tr[@class="d:f fld:c desktop(d:tr) bdc:grey-5 bd-b:1"]')
    print(len(check_length))
    if (len(check_length) == 1):
        # no affiliation info
        school_type = driver.find_elements(By.XPATH, '//tr[@class="d:f fld:c desktop(d:tr) bdc:grey-5 bd-b:1"]')[0].text
        affiliation = ''
    elif (len(check_length) == 2):
        # affiliation info exists
        affiliation =  driver.find_elements(By.XPATH, '//tr[@class="d:f fld:c desktop(d:tr) bdc:grey-5 bd-b:1"]')[0].text
        school_type = driver.find_elements(By.XPATH, '//tr[@class="d:f fld:c desktop(d:tr) bdc:grey-5 bd-b:1"]')[1].text
    else:
        # error
        quit()
    
    school_nature = driver.find_elements(By.XPATH, '//tr[@class="d:f fld:c desktop(d:tr)"]')[0].text

    return affiliation, school_nature, school_type


if __name__ == '__main__':
    url = "https://www.moe.gov.sg/schoolfinder?journey=Primary%20school"

    # Configure chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver =  webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'driver-close-btn'))).click()
    
    main_window = driver.window_handles[0]

    data = []

    for i in range(10):
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'moe-option-searchbar-input')))
        time.sleep(1)
        table = driver.find_elements(By.CLASS_NAME, "moe-school-card-animation")[0]
        all_links = table.find_elements(By.TAG_NAME, "a")
        print(len(all_links))

        p_bar = tqdm(total=len(all_links), desc=f'Scraping Page {i+1}/10')
        for link in all_links:
            time.sleep(1)
            link.click()
            driver.switch_to.window(driver.window_handles[1])

            school_name = driver.find_elements(By.TAG_NAME, "h1")[1].text
            programmes = get_programme_details()
            cca = get_cca_details()
            affiliation, school_nature, school_type = get_school_info()

            values = {'Name': school_name,
                      'Affiliation': affiliation,
                      'School_Nature': school_nature,
                      'School_Type': school_type,
                      'Programmes': programmes,
                      'CCA': cca}
            
            data.append(values)
            p_bar.update(1)

            driver.close()
            driver.switch_to.window(main_window)

        page_button = driver.find_elements(By.CLASS_NAME, "moe-pagination")[0]
        page_button.find_elements(By.TAG_NAME, 'button')[1].click()

    df = pd.DataFrame(data)

    df.to_csv("../../data/school-details.csv", index=False)
    