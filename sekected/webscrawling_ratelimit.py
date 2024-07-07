# interest_rate_spider.py

# import scrapy
# from scrapy import signals
# from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from NorenApi import NorenApi

# Initialize API
api = NorenApi()

user_id = 'FA108224'
user_pwd = 'Ram39#Kils'
token = open("shoonyakey.txt", 'r').read().strip()
api.set_session(userid=user_id, password=user_pwd, usertoken=token)

# Fetch historical volatility
def get_historical_volatility(symbol, period="1y"):
    data = yf.download(symbol, period=period)
    data['Returns'] = data['Adj Close'].pct_change()
    volatility = np.std(data['Returns']) * np.sqrt(252)
    return volatility

print("get_historical_volatility", get_historical_volatility(symbol='^NSEBANK'))

class InterestRateSpider(scrapy.Spider):
    name = 'interest_rate_spider'
    start_urls = [
        "https://www.investing.com/rates-bonds/india-10-year-bond-yield",
        "https://www.rbi.org.in/Scripts/BS_NSDPDisplay.aspx?param=4"
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Delay between requests
        'CONCURRENT_REQUESTS': 1,  # Number of concurrent requests
        'RETRY_TIMES': 3  # Number of retry attempts
    }

    def parse(self, response):
        if "investing.com" in response.url:
            interest_rate = self.parse_investing(response)
        elif "rbi.org.in" in response.url:
            interest_rate = self.parse_rbi(response)

        print(f"Interest rate from {response.url}: {interest_rate}")
        yield {'url': response.url, 'interest_rate': interest_rate}

    def parse_investing(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        interest_rate = None
        try:
            interest_rate_element = soup.find("span", {"data-test": "instrument-price-last"})
            if interest_rate_element:
                interest_rate = interest_rate_element.text.strip('%')
        except Exception as e:
            self.logger.error(f"First selector failed: {e}")

        if interest_rate is None:
            try:
                interest_rate_element = soup.find("div", {"data-test": "instrument-price-last"})
                if interest_rate_element:
                    interest_rate = interest_rate_element.text.strip('%')
            except Exception as e:
                self.logger.error(f"Second selector failed: {e}")

        if interest_rate is not None:
            return float(interest_rate) / 100  # Convert to decimal
        else:
            self.logger.error("Interest rate element not found.")
            return None

    def parse_rbi(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find_all('tr')
        interest_rate = None
        for row in table_rows:
            cells = row.find_all('td')
            if cells and cells[0].text.strip() == "10-Year G-Sec Par Yield (FBIL)":
                interest_rate = cells[-1].text.strip()
                break

        if interest_rate is not None:
            return float(interest_rate) / 100  # Convert to decimal
        else:
            self.logger.error("Interest rate not found in HTML table.")
            return None

process = CrawlerProcess()
process.crawl(InterestRateSpider)
process.start()

# Example usage
volatility = get_historical_volatility(symbol='^NSEBANK')

# Fetch current interest rate using Scrapy
interest_rate = None

# Retrieve the scraped data from the CrawlerProcess
for result in process:
    interest_rate = result.get('interest_rate')
    if interest_rate:
        break

if interest_rate is not None:
    print(f"Interest Rate: {interest_rate:.4f}")
else:
    print("Failed to retrieve the interest rate.")

# Now you can use these values in your API call
if interest_rate is not None and volatility is not None:
    ret = api.option_greek(
        expiredate='3-JUL-2024',
        StrikePrice='52300',
        SpotPrice='52342.25',
        InterestRate=f'{interest_rate:.4f}',
        Volatility=f'{volatility:.2f}',
        OptionType='CE'
    )
    print(f"option greeks :  {ret}")
else:
    print("Failed to retrieve required data for API call.")
