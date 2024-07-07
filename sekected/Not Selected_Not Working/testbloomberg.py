import requests
from bs4 import BeautifulSoup

def get_interest_rate_bloomberg():
    url = "https://www.bloomberg.com/markets/rates-bonds/government-bonds/asia-pacific"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table container with class "table-container"
        table_container = soup.find("div", class_='table-container')
        
        print("table_container " , table_container)
        
        # Find the specific section with class "table-container__title" for "Asia Pacific"
        section_title = table_container.find( class_="table-container__title", text="Asia Pacific")
        # table_container.
        
        if section_title:
            print("hhhhh")
            # Find the table rows (tr) within the same parent as the section title
            rows = section_title.find_next_sibling("table", class_="data-table").find("tbody").find_all("tr")
            
            # Loop through each row to find the one with "India"
            for row in rows:
                country_cell = row.find("div", class_="data-table-row-cell__link-block", text="India")
                if country_cell:
                    # Once India is found, get the corresponding interest rate
                    interest_rate_element = row.find("span", class_="data-table-row-cell__value")
                    if interest_rate_element:
                        interest_rate = interest_rate_element.text.strip()
                        return interest_rate
                    else:
                        raise ValueError("Interest rate element not found.")
            
            # If India is not found
            raise ValueError("India interest rate not found in the Asia Pacific section.")
        else:
            raise ValueError("Asia Pacific section title not found.")
    
    except Exception as e:
        print(f"Error fetching interest rate from Bloomberg: {e}")
        return None

# Example usage
interest_rate = get_interest_rate_bloomberg()
if interest_rate is not None:
    print(f"Interest Rate for India: {interest_rate}")
else:
    print("Failed to retrieve the interest rate.")
