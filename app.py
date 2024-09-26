#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

# import requests
# from bs4 import BeautifulSoup

# url = 'https://www.autovit.ro/autoturisme/porsche/cayenne-coupe'
# headers = {'User-Agent': 'ScraperTest'}
# robots_url = f'{url}/robots.txt'

# def scrape_mobile_de():
#     robots = requests.get(robots_url).text
#     if 'Disallow: /' in robots:
#         print("Scraping not allowed by robots.txt")
#         return

#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         articles = soup.select('div[data-testid="search-results"] > div > article')
#         for article in articles:
#             # articleSoup = BeautifulSoup(article, 'html.parser')
#             # Extract the title
#             title = article.select_one('h1 a').text
#             print("Title:", title)

#             # Extract the mileage
#             mileage = article.select_one('dd[data-parameter="mileage"]').text
#             print("Mileage:", mileage)

#             # Extract the fuel type
#             fuel_type = article.select_one('dd[data-parameter="fuel_type"]').text
#             print("Fuel Type:", fuel_type)

#             # Extract the price
#             price = article.select_one('h3').text
#             print("Price: ", price)
#             print("---------------------------------")
#     else:
#         print(f"Failed to access {url} {response.reason}")

# scrape_mobile_de()
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# Set up Chrome options for headless browsing (required for AWS Lambda)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Required in most environments like AWS Lambda
chrome_options.add_argument("--disable-dev-shm-usage")  # Helps avoid issues with shared memory
chrome_options.add_argument("--remote-debugging-port=9222")  # Opens the debugging port required by headless Chrome
chrome_options.add_argument("--window-size=1920x1080")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# In AWS Lambda, you'll need to include the binary location if required
# chrome_options.binary_location = '/opt/chrome/chrome'

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.autovit.ro/autoturisme/porsche/cayenne-coupe'
url2 = 'https://www.autovit.ro/autoturisme/bmw/i7'
robots_url = 'https://www.autovit.ro/robots.txt'  # Corrected robots.txt URL

# Function to check robots.txt
def check_robots():
    # robots_txt = requests.get(robots_url).text
    # if 'Disallow: /' in robots_txt:
    #     print("Scraping is disallowed by robots.txt")
    #     return False
    return True

# Results array to collect all scraped data
results = []

def scrape_page():
    print("Scrapes data from the current page.")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select('div[data-testid="search-results"] > div > article')
    
    for article in articles:
        try:
            title = article.select_one('h1 a').text.strip()
            mileage = article.select_one('dd[data-parameter="mileage"]').text.strip()
            fuel_type = article.select_one('dd[data-parameter="fuel_type"]').text.strip()
            price = article.select_one('h3').text.strip()

            results.append({
                "title": title,
                "mileage": mileage,
                "fuel_type": fuel_type,
                "price": price
            })
        except AttributeError:
            # In case any element is not found, we skip it
            pass

def click_next_page(current_page_num):
    
    next_page_selector = f'li[aria-label="Page {current_page_num + 1}"] span'
    print(f"Clicks on the next page {current_page_num + 1}")
    try:
        # Find the next page element and click it
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page = driver.find_element(By.CSS_SELECTOR, next_page_selector)
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(4)
        # next_page.click()
        # time.sleep(4)  # Allow the page to load fully before scraping again
        return True
    except Exception as e:
        # print(f"No more pages found in source: {str(e)}")
        return False

def scrape_all_pages():
    
    current_page_num = 1
    print(f'Scrape all pages until no more next page buttons exist. Current page {current_page_num}')
    while True:
        # Scrape current page
        scrape_page()

        # Try to click to the next page
        if not click_next_page(current_page_num):
            break
        current_page_num += 1

# Start by checking robots.txt before proceeding
if check_robots():
    # Start scraping all pages
    driver.get(url2)
    time.sleep(5)
    print("opened")
    scrape_all_pages()

    # Close the browser after scraping is done
    driver.quit()

    # Print the collected results
    for result in results:
        print(result)
else:
    print("Exiting... Robots.txt disallows scraping.")

