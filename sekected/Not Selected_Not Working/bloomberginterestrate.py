from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def extract_interest_rate_from_bloomberg(url):
    try:
        # Set up Selenium options
        options = Options()
        options.headless = True
        service = Service('/path/to/chromedriver')  # Update this path to your chromedriver

        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Go to the Bloomberg URL
        driver.get(url)
        
        # Wait for the table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'data-table-row'))
        )
        
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Close the Selenium driver
        driver.quit()
        
        # Find all table rows
        table_rows = soup.find_all('tr', class_='data-table-row')
        print("table_rows:", table_rows)
        
        interest_rate = None
        
        # Look for the specific row containing "India"
        for row in table_rows:
            if row.find('div', class_='data-table-row-cell__link-block', attrs={'data-type': 'full'}) and "India" in row.text:
                print(row.text)
                # Extract the interest rate from the specific <td> and <span> structure
                td_cell = row.find('td', class_='data-table-row-cell', attrs={'data-type': 'percent', 'aria-label': 'percent'})
                if td_cell and td_cell.find('span', class_='data-table-row-cell__value'):
                    interest_rate = td_cell.find('span', class_='data-table-row-cell__value').text.strip()
                    break  # Found the interest rate, exit the loop
        
        if interest_rate is None:
            raise ValueError("Interest rate not found in HTML table.")
        
        return interest_rate, "Bloomberg"
    
    except Exception as e:
        print(f"Error extracting interest rate from Bloomberg: {e}")
        return None, "Bloomberg"

# URL for Bloomberg data
url_bloomberg = "https://www.bloomberg.com/markets/rates-bonds/government-bonds/india"

# Extract interest rate from Bloomberg
interest_rate, source = extract_interest_rate_from_bloomberg(url_bloomberg)
if interest_rate is not None:
    print(f"Interest rate: {interest_rate} (Source: {source})")
else:
    print("Failed to retrieve interest rate from Bloomberg.")
