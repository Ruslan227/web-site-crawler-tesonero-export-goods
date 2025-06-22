import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import logging
from secrets_utils import get_secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from secrets
secrets = get_secrets()
BASE_URL = secrets["BASE_URL"]
OUTPUT_FILE = secrets.get("OUTPUT_FILE", 'products.xlsx')

TAB_NAMES = [secrets["PRODUCT_TYPE1_TAB_NAME"], secrets["PRODUCT_TYPE2_TAB_NAME"]]
TAB_CONFIG = [(name, f'button:has-text("{name}")') for name in TAB_NAMES]

def get_random_delay():
    """Return random delay between 3-8 seconds"""
    return random.uniform(3, 8)

def scrape_categories(page):
    """Scrape all product categories from both tabs using Playwright"""
    logging.info("Scraping categories with Playwright...")
    try:
        page.goto(f"{BASE_URL}/catalog", timeout=60000)
        page.wait_for_selector('.catalog-products__btn', timeout=15000)
        
        categories = []
        
        for tab_name, tab_selector in TAB_CONFIG:
            try:
                # Switch to the tab
                tab_button = page.query_selector(tab_selector)
                if not tab_button:
                    logging.warning(f"Tab button not found: {tab_name}")
                    continue
                    
                # Check if tab is active
                is_active = "catalog-products__btn_active" in (
                    tab_button.get_attribute("class") or ""
                )
                
                # Activate tab if needed
                if not is_active:
                    tab_button.click()
                    # Wait for content to load
                    page.wait_for_selector('.catalog-item__title', timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=3000)
                
                # Extract category elements
                category_elements = page.query_selector_all('.catalog-item__title')
                
                for element in category_elements:
                    name = element.inner_text().strip()
                    url = urljoin(BASE_URL, element.get_attribute('href'))
                    categories.append({'type': f"{tab_name}: {name}", 'url': url})
                    
                logging.info(f"Found {len(category_elements)} categories in {tab_name} tab")
                
            except Exception as e:
                logging.error(f"Error scraping {tab_name} tab: {e}")
                # Save page for debugging
                page.screenshot(path=f"tab_error_{tab_name}.png", full_page=True)
        
        logging.info(f"Total categories found: {len(categories)}")
        return categories
        
    except Exception as e:
        logging.error(f"Error scraping categories: {e}")
        return []

def scrape_product_listing(page, category_url, category_name):
    """Scrape all products from a category listing page"""
    logging.info(f"Scraping product listing for {category_name}")
    try:
        page.goto(category_url, timeout=60000)
        page.wait_for_selector('.products-recent-item_catalog', timeout=15000)
        
        # Extract product cards
        products = []
        product_cards = page.query_selector_all('.products-recent-item_catalog')
        
        for card in product_cards:
            try:
                # Extract elements directly from Playwright
                name_element = card.query_selector('.products-recent__name_catalog')
                price_element = card.query_selector('.products-recent__price_catalog')
                material_element = card.query_selector('.products-recent__parameter-item_secondary')
                
                # Extract text content
                name = name_element.inner_text().strip() if name_element else ''
                price = price_element.inner_text().strip() if price_element else ''
                material = material_element.inner_text().strip() if material_element else ''
                url = urljoin(BASE_URL, name_element.get_attribute('href')) if name_element else ''
                
                # Extract dimensions, SKU, and stock
                dimensions = ''
                sku = ''
                stock = ''
                
                param_elements = card.query_selector_all('.products-recent__parameter_catalog')
                for param in param_elements:
                    text = param.inner_text().strip()
                    if "Размеры:" in text:
                        dimensions = text.replace("Размеры:", "").strip()
                    elif "Артикул:" in text:
                        sku = text.replace("Артикул:", "").strip()
                    elif "На складе:" in text:
                        stock = text.replace("На складе:", "").strip()
                
                products.append({
                    'category': category_name,
                    'name': name,
                    'url': url,
                    'price': price,
                    'material': material,
                    'dimensions': dimensions,
                    'sku': sku,
                    'stock': stock
                })
            except Exception as e:
                logging.warning(f"Error parsing product card: {e}")
                
        logging.info(f"Found {len(products)} products in {category_name}")
        return products
    except Exception as e:
        logging.error(f"Error scraping product listing: {e}")
        return []

def scrape_product_detail(page, product):
    """Scrape detailed information from product page including description"""
    logging.info(f"Scraping product details: {product['name']}")
    try:
        page.goto(product['url'], timeout=60000)
        page.wait_for_selector('.product-info-desc__title', timeout=15000)
        
        # Extract detailed info
        name_element = page.query_selector('.product-info-desc__title')
        price_element = page.query_selector('.product-info-desc__price')
        char_items = page.query_selector_all('ul.product-info-details__desc > li')
        
        # Extract text content
        detailed_name = name_element.inner_text().strip() if name_element else product['name']
        detailed_price = price_element.inner_text().strip() if price_element else product['price']
        
        # Extract characteristics
        characteristics = []
        for char in char_items:
            title_element = char.query_selector('.product-info-details__title')
            value_element = char.query_selector('.product-info-details__value')
            if title_element and value_element:
                title = title_element.inner_text().strip()
                value = value_element.inner_text().strip()
                characteristics.append(f"{title}: {value}")
        
        # Enhanced description extraction
        description = ""
        try:
            # Locate description tab
            desc_tab = page.query_selector('.product-info-details__tab:has-text("Описание")')
            if not desc_tab:
                logging.warning(f"No description tab found for {product['name']}")
                raise Exception("Description tab missing")
            
            # Check active state
            is_active = "product-info-details__tab_active" in (desc_tab.get_attribute("class") or "")
            
            # Activate tab if needed
            if not is_active:
                # Click with error handling
                try:
                    desc_tab.click(timeout=3000)
                    page.wait_for_load_state("networkidle", timeout=5000)
                except Exception as e:
                    logging.warning(f"Tab click failed: {e}. Retrying...")
                    page.evaluate('document.querySelector(\'.product-info-details__tab:has-text("Описание")\').click()')
                    page.wait_for_timeout(2000)
                
                # Wait for content to appear
                page.wait_for_selector('.product-info-details__description', state="attached", timeout=5000)
            
            # Wait until description has content
            page.wait_for_function(
                '() => { '
                '  const desc = document.querySelector(".product-info-details__description"); '
                '  return desc && desc.innerText.trim().length > 0; '
                '}', 
                timeout=8000
            )
            
            # Extract description
            desc_container = page.query_selector('.product-info-details__description')
            if desc_container:
                description = desc_container.inner_text().strip()
            else:
                logging.warning("Description container found but empty")
        except Exception as e:
            logging.error(f"Description extraction failed: {e}")
            try:
                # Fallback: Try to extract any visible description
                desc_container = page.query_selector('.product-info-details__description')
                if desc_container and desc_container.is_visible():
                    description = desc_container.inner_text().strip()
            except:
                pass
                
        return {
            **product,
            'detailed_name': detailed_name,
            'detailed_price': detailed_price,
            'characteristics': "; ".join(characteristics),
            'description': description
        }
    except Exception as e:
        logging.error(f"Error scraping product details: {e}")
        return product

def main():
    """Main scraping workflow"""

    logging.info(f"Starting scraper with configuration:")
    logging.info(f"  BASE_URL: {BASE_URL}")
    logging.info(f"  OUTPUT_FILE: {OUTPUT_FILE}")
    logging.info(f"  TABS: {TAB_NAMES}")

    with sync_playwright() as playwright:
        # Launch browser (set headless=False to see the browser)
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Step 1: Get all categories
        categories = scrape_categories(page)
        if not categories:
            logging.error("No categories found. Exiting.")
            return
            
        all_products = []
        
        # Step 2: Scrape each category
        for i, category in enumerate(categories):
            time.sleep(get_random_delay())
            logging.info(f"Processing category {i+1}/{len(categories)}: {category['type']}")
            
            products = scrape_product_listing(page, category['url'], category['type'])
            
            # Step 3: Scrape individual product details
            for j, product in enumerate(products):
                time.sleep(get_random_delay())
                detailed_product = scrape_product_detail(page, product)
                all_products.append(detailed_product)
                logging.info(f"  Scraped product {j+1}/{len(products)}: {detailed_product['name']}")
        
        # Step 4: Export to Excel
        if all_products:
            df = pd.DataFrame(all_products)
            df.to_excel(OUTPUT_FILE, index=False, engine='openpyxl')
            logging.info(f"Success! Exported {len(df)} products to {OUTPUT_FILE}")
        else:
            logging.error("No products scraped.")
        
        # Close browser
        context.close()
        browser.close()

if __name__ == "__main__":
    main()