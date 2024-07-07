import yfinance as yf
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from NorenApi import NorenApi




# Fetch historical volatility
def get_historical_volatility(symbol, period="1y"):
    data = yf.download(symbol, period=period)
    # print("yf data " , data)
    data['Returns'] = data['Adj Close'].pct_change()
    # print("yf data " ,  data['Returns'])
    volatility = np.std(data['Returns']) * np.sqrt(252)
    return volatility

# print(" get_historical_volatility ", get_historical_volatility(symbol='^NSEBANK'))


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Fetch current interest rate from Investing.com
def get_interest_rate_investing():
    url = "https://www.investing.com/rates-bonds/india-10-year-bond-yield"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different selectors sequentially
        interest_rate = None
        try:
            interest_rate_element = soup.find("span", {"data-test": "instrument-price-last"})
            if interest_rate_element:
                interest_rate = interest_rate_element.text.strip('%')
        except Exception as e:
            print(f"First selector failed: {e}")

        if interest_rate is None:
            try:
                interest_rate_element = soup.find("div", {"data-test": "instrument-price-last"})
                if interest_rate_element:
                    interest_rate = interest_rate_element.text.strip('%')
            except Exception as e:
                print(f"Second selector failed: {e}")

        if interest_rate is not None:
            return float(interest_rate) / 100  # Convert to decimal
        else:
            raise ValueError("Interest rate element not found.")
    except Exception as e:
        print(f"Error fetching interest rate from Investing.com: {e}")
        return None

def extract_interest_rate_from_RBI():
    url = "https://www.rbi.org.in/Scripts/BS_NSDPDisplay.aspx?param=4"
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table rows
        table_rows = soup.find_all('tr')
        
        interest_rate = None
        
        # Look for the specific row containing "10-Year G-Sec Par Yield (FBIL)"
        for row in table_rows:
            # Extract all <td> cells in the row
            cells = row.find_all('td')
            
            # Check if the first cell contains "10-Year G-Sec Par Yield (FBIL)"
            if cells and cells[0].text.strip() == "10-Year G-Sec Par Yield (FBIL)":
                # Extract the text from the last cell (last column)
                interest_rate = cells[-1].text.strip()
                break  # Found the interest rate, exit the loop
        
        if interest_rate is None:
            raise ValueError("Interest rate not found in HTML table.")
        
        return float(interest_rate) / 100  # Convert to decimal
    
    except Exception as e:
        print(f"Error extracting interest rate from HTML: {e}")
        return None, "HTML"
    
def get_current_interest_rate():
    sources = [get_interest_rate_investing, extract_interest_rate_from_RBI]
    for source in sources:
        interest_rate = source()
        if interest_rate is not None:
            return interest_rate
    print("Failed to retrieve the interest rate from all sources.")
    return None


# Example usage
# print(" get_historical_volatility ", get_historical_volatility(symbol='^NSEBANK'))
volatility=get_historical_volatility(symbol='^NSEBANK')
interest_rate = get_current_interest_rate()   



class recieveltp():
    # def __init__(self, ltp,tkn):
    #     self.ltp=ltp
    #     self.tkn=tkn
    # Initialize API
    
    # self.api=NorenApi()
    
    async def PrintRecieved_ltp(self,ltp,tkn):
        print("\n LTP " , ltp)
        print("\n tkn " , tkn)
        # print("\n exch  NSE")
        
    
   
    async def get_optionGreek(self,ltp, interest_rate=interest_rate, volatility= volatility):
        # volatility=get_historical_volatility(symbol='^NSEBANK')
        # interest_rate = get_current_interest_rate()   
        # if interest_rate is not None:
        #     # print(f"Interest Rate: {interest_rate:.4f}")
        # else:
        #     print("Failed to retrieve the interest rate.")
            
        if interest_rate is None:
            print("Failed to retrieve the interest rate.")
            # Now you can use these values in your API call
        
        if interest_rate is not None and volatility is not None:
            api = NorenApi()
            user_id = 'FA108224'
            user_pwd = 'Ram39#Kils'
            token = open("shoonyakey.txt", 'r').read().strip()
            # print("token ", token)
            # self.api=NorenApi()
            api.set_session(userid=user_id, password=user_pwd, usertoken=token)
            
            ret = api.option_greek(
                expiredate='10-JUL-2024',
                StrikePrice='53100',
                SpotPrice=ltp,
                InterestRate=f'{interest_rate:.6f}',
                Volatility=f'{volatility:.6f}',
                OptionType='CE'
            )
            print(f"option greeks : \n {ret} \n")
        else:
            print("Failed to retrieve required data for API call.")
    # # Now you can use these values in your API call
    # ret = api.option_greek(
    #     expiredate='3-JUL-2024',
    #     StrikePrice='52300',
    #     SpotPrice='52342.25',
    #     InterestRate=f'{interest_rate:.4f}',
    #     Volatility=f'{volatility:.2f}',
    #     OptionType='CE'
    # )
