from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_bse_market_overview():
    """Scrapes overall market data like market capitalization from BSE using Selenium."""
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

        # Wait for the page to load (adjust timeout as needed)
        driver.implicitly_wait(10)

        # Extract page source
        html = driver.page_source
        driver.quit()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", {"class": "table table-bordered table-striped"})
        if not table:
            raise ValueError("Market data table not found on the page.")

        # Extract data from the table
        rows = table.find_all("tr")
        market_data = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                market_data[key] = value

        # Extract specific metrics
        total_market_cap = market_data.get("All India Market Capitalisation (Rs.Cr)", "Data not available")
        top_10_market_cap = market_data.get("Top 10 Companies Market Capitalisation (Rs.Cr.)", "Data not available")

        return {
            "total_market_cap": total_market_cap,
            "top_10_market_cap": top_10_market_cap
        }

    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None
