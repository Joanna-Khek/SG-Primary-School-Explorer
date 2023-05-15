# Selenium Web Scraping
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from tqdm import tqdm
import re

def numbers_exist(s):
    return any(i.isdigit() for i in s)

def remove_brackets(s):
    return re.sub("\(.*?\)", "", s)

def remove_symbols(s):
    s = s.replace("↳ ", "")
    s = re.sub(f"\n\nSC<\d+", "", s)
    s = re.sub(f"\n\nSC>\d+", "", s)
    s = re.sub(f"\n\nPR<\d+", "", s)
    s = re.sub(f"\n\nPR>\d+", "", s)
    s = re.sub(f"\n\nSC1-2", "", s)
    s = re.sub(f"\n\nSC#", "", s)
    s = re.sub(f"\n\nPR#", "", s)
    s = re.sub(f"\n\nSC\d+#", "", s)
    s = re.sub(f"\n\nPR<\d+#", "", s)
    s = s.replace("#", "")
    return s


def extract_information():

    url = "https://sgschooling.com/year/2022/all.html"

    # setting up options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver =  webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "header__logo")))

    # obtain table id
    table_id = driver.find_elements(By.TAG_NAME, "table")[0]
    rows = table_id.find_elements(By.TAG_NAME, "tr")[1:]

    school_name = []
    vacancy_list = []
    applied_list = []
    taken_list = []

    p_bar = tqdm(total = len(rows), desc="Extracting...")
    for row in rows:
        if numbers_exist(row.text) == False:
            s = row.text.strip()
            school_name.append(s)
        
        if 'Vacancy' in row.text:
            s = remove_symbols(row.text)
            s = remove_brackets(s)
            vacancy_list.append(s)

        if 'Applied' in row.text:
            s = remove_symbols(row.text)
            applied_list.append(s)

        if 'Taken' in row.text:
            s = remove_symbols(row.text)
            taken_list.append(s)
        
        p_bar.update(1)

    df = dict()
    df['School_Name'] = school_name
    df['Vacancy'] = vacancy_list
    df['Applied'] = applied_list
    df['Taken'] = taken_list

    return pd.DataFrame(df)

def preprocess_data(df):
    # Clean vacancy data 
    df_vacancy_clean = (df
                    .Vacancy.str.split(" ", expand=True)
                    .drop([0, 1], axis=1)
    )
    df_vacancy_clean.columns = ['Phase1_vac', 'Phase2A_vac', 'Phase2B_vac', 'Phase2C_vac', 
                                'Phase2CS_vac', 'Phase3_vac']

    # Clean applied data
    df_applied_clean = (df
                        .Applied.str.split(" ", expand=True)
                        .drop(0, axis=1)
    )
    df_applied_clean.columns = ['Phase1_applied', 'Phase2A_applied', 'Phase2B_applied', 
                                'Phase2C_applied', 'Phase2CS_applied', 'Phase3_applied']
    
    # Clean Taken data
    df_taken_clean = (df
                      .Taken.str.split(" ", expand=True)
                      .drop(0, axis=1)
    )

    df_taken_clean.columns = ['Phase1_taken', 'Phase2A_taken', 'Phase2B_taken',
                              'Phase2C_taken', 'Phase2CS_taken', 'Phase3_taken']
    

    df_clean = pd.concat([df.School_Name, df_vacancy_clean, df_applied_clean, df_taken_clean], axis=1)

    return df_clean

if __name__ == '__main__':

    df = extract_information()
    df_clean = preprocess_data(df)

    # Save
    df_clean.to_csv("../../data/raw/vacancy-data.csv", index=False, encoding='utf-8-sig')