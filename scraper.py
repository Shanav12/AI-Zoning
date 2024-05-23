from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from bs4 import BeautifulSoup
from config import chromedriver_path

# Since this site is loaded dynamically and requires Javascript execution, we will need a ChromeDriver to scrape from it
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URLs for each section of the ordinance that we will be scraping
section_urls = {
    'CODE OF ORDINANCES TOWN OF GREENVILLE, FLORIDA' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=COORTOGRFL_GREENVILLE_OFFICIALS',
    'SUPPLEMENT HISTORY TABLE' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=SUHITA',
    'CHARTER COMPARATIVE TABLE' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=CHTR_COMPARATIVE_TABLELE',
    'Part I - CHARTER' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTICH',
    'Chapter 1': 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH1GEPR',
    'Chapter 2': 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH2AD',
    'Chapter 4': 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH2AD',
    'Chapter 6' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH6ANFO',
    'Chapter 8' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH8BU',
    'Chapter 10' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH10BURE',
    'Chapter 12' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH12FIPR',
    'Chapter 14' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH14HURE',
    'Chapter 16' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH16NUDABUHALA',
    'Chapter 18' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH18OFMIPR',
    'Chapter 20' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH20SOWA',
    'Chapter 22' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH22STSIPUPL',
    'Chapter 24' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH24TA',
    'Chapter 26' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_CH26UTCAELNAGA',
    'Appendix A - FEE SCHEDULE FOR THE TOWN OF GREENVILLE, FLORIDA' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=PTIICOOR_APXAFESCTOGRFL',
    'CODE COMPARATIVE TABLE - LEGISLATION' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=CD_COMPARATIVE_TABLELE',
    'STATE LAW REFERENCE TABLE' : 'https://library.municode.com/fl/greenville/codes/code_of_ordinances?nodeId=STLARETA'
}

# Specifying the output directory of the txt file, if it does not exist we will create it
output_directory = 'Greenville-Ordinance'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Given a url and a section name, we will be scraping all of the text from that section
def scrape_section(url, section_name):
    try:
        driver.get(url)
        # We will wait 30 seconds until we've located the chunk-title class name in the html, as this class is found in each url
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'chunk-title'))
        )
        html_content = driver.page_source
        # We will use BeautifulSoup in order to parse the html returned and extract the desired text
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract the text we desire based on class names in the html code
        text = []
        # Each header has this class name in their div tag
        chunks = soup.find_all('div', class_='chunk-title')
        for chunk in chunks:
            title = chunk.get_text(strip=True)
            text.append(title)
            # The text is placed under div tags with this class name, we will be extracting them to place alongside their header
            content_div = chunk.find_next('div', class_='chunk-content')
            if content_div:
                text.append('\n')
                # These are the class names with the relevant text, any p tag with a class from this list will be extracted
                for p in content_div.find_all('p', class_=['p0', 'content2', 'content1', 'historynote0']):
                    text.append(p.get_text(strip=True))
                # Adding a horizontal line between chunks to be more readable, will also use in tree building
                text.append('-' * 50)
        # Joining the text list into a single string and writing it to the specified file in append mode
        text_content = '\n'.join(text)
        with open(f'{output_directory}/Ordinance.txt', 'a') as file:
            file.write(text_content)
            # Delimiter to place in between each section
            file.write('\n\n\n\n')
        print(f'Scraped content for {section_name} has been written.')
    except Exception as e:
        print(f'Failed to scrape {section_name}: {e}')
    
# Iterating through each section and using their url to scrape text from
for section_name, url in section_urls.items():
    scrape_section(url, section_name)

# Closing the web driver after we've finished scraping
driver.quit()