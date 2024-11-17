from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_bse_market_overview():
    """Scrape market data from BSE's All India Market Capitalization page using Selenium."""
    url = "https://www.bseindia.com/markets/equity/eqreports/allindiamktcap.aspx"

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    try:
        # Use Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load fully (adjust timeout as needed)
        driver.implicitly_wait(10)

        # Extract page source after JavaScript execution
        html = driver.page_source
        driver.quit()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", {"id": "ContentPlaceHolder1_gvData"})
        if not table:
            raise ValueError("Market data table not found.")

        # Extract rows from the table
        rows = table.find_all("tr")
        if len(rows) < 2:
            raise ValueError("No data rows found in the table.")

        # Parse the first data row
        data_row = rows[1]
        cells = data_row.find_all("td")

        # Extract individual values
        total_companies = cells[0].get_text(strip=True)
        total_market_cap = cells[1].get_text(strip=True)
        top_10_market_cap = cells[2].get_text(strip=True)

        return {
            "total_companies": total_companies,
            "total_market_cap": total_market_cap,
            "top_10_market_cap": top_10_market_cap
        }

    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

# if __name__ == "__main__":
#     market_data = get_bse_market_overview()
#     print("Market Overview Data:", market_data)