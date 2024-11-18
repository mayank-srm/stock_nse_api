from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_bse_market_overview():
    """Scrape BSE All India Market Capitalization data."""
    url = "https://www.bseindia.com/markets/equity/eqreports/allindiamktcap.aspx"

    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Allow time for the page to load
    time.sleep(5)

    # Extract page source
    html = driver.page_source
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(html, "lxml")

    # Locate the date element
    date_element = soup.find("span", id="ContentPlaceHolder1_lblDate")
    if not date_element:
        raise ValueError("Date element not found on the page.")
    as_on_date = date_element.get_text(strip=True).replace("As on ", "")

    # Locate the data table
    table = soup.find("table", id="ContentPlaceHolder1_gvData")
    if not table:
        raise ValueError("Market data table not found on the page.")

    # Extract data from the table
    rows = table.find_all("tr")
    if len(rows) < 2:
        raise ValueError("Insufficient data rows found in the table.")
    data_row = rows[1]
    cells = data_row.find_all("td")
    if len(cells) < 3:
        raise ValueError("Insufficient data columns found in the table.")

    # Extract and clean data
    total_companies = cells[0].get_text(strip=True)
    total_market_cap = cells[1].get_text(strip=True).replace(",", "")
    top_10_market_cap = cells[2].get_text(strip=True).replace(",", "")

    # Return the extracted data
    return {
        "as_on_date": as_on_date,
        "total_companies": total_companies,
        "total_market_cap": total_market_cap,
        "top_10_market_cap": top_10_market_cap
    }
