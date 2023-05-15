# Selenium Web Scraping
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time

def extract_school_details():
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    table_id = driver.find_element(By.XPATH, "//div[@class='moe-school-card-animation']").find_elements(By.TAG_NAME, "a")
    data_list = []
    for row in table_id:
        name = row.find_elements(By.TAG_NAME, "p")[0].text
        data_list.append(name)
        
    # Formatting
    df = pd.DataFrame(data_list)
    df = df.rename(columns={0: 'Name'})
    return df

def get_GEP_schools():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_elements(By.XPATH, "//div[@class='moe-sidebar-toggle m-b:m']")[3].click()
    time.sleep(1)
    driver.find_elements(By.XPATH, "//span[@class='checkmark type-grey-2']")[13].click()

    df_gep = extract_school_details()
    
    return df_gep

def get_IP_schools():
     
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     time.sleep(1)
     driver.find_elements(By.XPATH, "//div[@class='moe-sidebar-toggle m-b:m']")[3].click()
     time.sleep(1)
     driver.find_elements(By.XPATH, "//span[@class='checkmark type-grey-2']")[14].click()

     df_ip = extract_school_details()
     return df_ip



if __name__ == '__main__':
    url = "https://www.moe.gov.sg/schoolfinder?journey=Primary%20school"

    # Configure chrome options
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver =  webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'driver-close-btn'))).click()
    main_window = driver.window_handles[0]

    df_gep = get_GEP_schools()

    # refresh
    driver.get(url)

    df_ip = get_IP_schools()

    df_gep.to_csv("../../data/school-gep.csv", index=False)
    df_ip.to_csv("../../data/school-ip.csv", index=False)
    
    