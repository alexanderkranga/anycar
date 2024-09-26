#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

url = 'https://www.autovit.ro/autoturisme/porsche/cayenne-coupe'
headers = {'User-Agent': 'ScraperTest'}
robots_url = f'{url}/robots.txt'

def scrape_mobile_de():
    robots = requests.get(robots_url).text
    if 'Disallow: /' in robots:
        print("Scraping not allowed by robots.txt")
        return

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = soup.select('div[data-testid="search-results"] > div > article')
        for article in articles:
            # articleSoup = BeautifulSoup(article, 'html.parser')
            # Extract the title
            title = article.select_one('h1 a').text
            print("Title:", title)

            # Extract the mileage
            mileage = article.select_one('dd[data-parameter="mileage"]').text
            print("Mileage:", mileage)

            # Extract the fuel type
            fuel_type = article.select_one('dd[data-parameter="fuel_type"]').text
            print("Fuel Type:", fuel_type)

            # Extract the price
            price = article.select_one('h3').text
            print("Price: ", price)
            print("---------------------------------")
    else:
        print(f"Failed to access {url} {response.reason}")

scrape_mobile_de()