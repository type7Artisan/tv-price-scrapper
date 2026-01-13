import json
import logging
import asyncio
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from scrapers.costco_scraper import CostcoScraper
from scrapers.bestbuy_scraper import BestBuyScraper
from scrapers.amazon_scraper import AmazonScraper
from scrapers.visions_scraper import VisionsScraper
from scrapers.londondrugs_scraper import LondonDrugsScraper
from scrapers.canadiantire_scraper import CanadianTireScraper
from scrapers.dufresne_scraper import DufresneScraper
from scrapers.tanguay_scraper import TanguayScraper
from scrapers.teppermans_scraper import TeppermansScraper
from scrapers.lg_scraper import LGScraper
from scrapers.samsung_scraper import SamsungScraper
from scrapers.staples_scraper import StaplesScraper
from config.settings import DATA_DIR, RESULTS_DIR, CONCURRENT_REQUESTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PriceScraper:
    def __init__(self, retailer: str = 'all'):
        # Dictionary of available scrapers
        self.available_scrapers = {
            'visions': VisionsScraper,
            'canadiantire': CanadianTireScraper,
            'costco': CostcoScraper,
            'bestbuy': BestBuyScraper,
            'amazon': AmazonScraper,
            'londondrugs': LondonDrugsScraper,
            'dufresne': DufresneScraper,
            'tanguay': TanguayScraper,
            'teppermans': TeppermansScraper,
            'lg': LGScraper,
            'samsung': SamsungScraper,
            'staples': StaplesScraper,
            'all': None
        }

        # Initialize selected scrapers
        if retailer.lower() == 'all':
            self.scrapers = [
                scraper() for scraper in self.available_scrapers.values()
                if scraper is not None
            ]
        elif retailer.lower() in self.available_scrapers:
            self.scrapers = [self.available_scrapers[retailer.lower()]()]
        else:
            raise ValueError(f"Invalid retailer. Available options: {', '.join(self.available_scrapers.keys())}")

    async def scrape_product(self, product_name: str) -> List[Dict]:
        """Scrape prices for a single product"""
        results = []
        tasks = []

        for scraper in self.scrapers:
            task = asyncio.create_task(scraper.scrape(product_name))
            tasks.append(task)

        completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)

        for scraper, result in zip(self.scrapers, completed_tasks):
            if isinstance(result, Exception):
                logger.error(f"Error with {scraper.__class__.__name__}: {str(result)}")
                continue
            if result:
                results.extend(result)

        return results

    async def scrape_prices(self, products: List[Dict]) -> List[Dict]:
        """Scrape prices for multiple products"""
        all_results = []
        
        for product in products:
            product_name = product['name']
            logger.info(f"Scraping prices for: {product_name}")
            
            results = await self.scrape_product(product_name)
            
            if results:
                brand = results[0]['brand']
                all_results.append({
                    'Brand': brand,
                    'Product': [
                        {
                            'Website': r['website'],
                            'Title': r['title'],
                            'Price': r['price'],
                            'PriceValidTill': r.get('price_valid_till', ''),
                            'URL': r.get('url', '')
                        }
                        for r in results
                    ]
                })
            
        return all_results

    def save_results(self, results: List[Dict], filename: str = None):
        """Save results to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            retailer_name = 'all' if len(self.scrapers) > 1 else self.scrapers[0].__class__.__name__.lower().replace('scraper', '')
            filename = f'data/results/{retailer_name}_prices_{timestamp}.json'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")

async def main():
    # Get user input for retailer
    print("\nAvailable retailers:")
    print("- all (scrape from all retailers)")
    print("- visions")
    print("- canadiantire")
    print("- costco")
    print("- bestbuy")
    print("- amazon")
    print("- londondrugs")
    print("- dufresne")
    print("- tanguay")
    print("- teppermans")
    print("- lg")
    print("- samsung")
    print("- staples")
    
    retailer = input("\nEnter retailer name (or 'all' for all retailers): ").strip().lower()
    
    # Ask user for input method
    print("\nChoose input method:")
    print("1. Enter single product name")
    print("2. Load products from JSON file")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        # Single product input
        product = input("\nEnter product name (e.g. Samsung 65\" 4K Tizen Smart QLED TV - QN65Q60DAFXZC): ").strip()
        products = [{"name": product}]
    elif choice == "2":
        # JSON file input
        file_path = input("\nEnter path to JSON file (e.g., products.json): ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
                if not isinstance(products, list):
                    print("Error: JSON file must contain an array of products")
                    return
                # Verify each product has a name field
                for product in products:
                    if not isinstance(product, dict) or 'name' not in product:
                        print("Error: Each product must have a 'name' field")
                        return
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            return
    else:
        print("Invalid choice")
        return

    try:
        scraper = PriceScraper(retailer)
        results = await scraper.scrape_prices(products)
        scraper.save_results(results)
        
        # Print results to console
        print("\nResults:")
        for result in results:
            print(f"\nBrand: {result['Brand']}")
            for product in result['Product']:
                print(f"Website: {product['Website']}")
                print(f"Title: {product['Title']}")
                print(f"Price: ${product['Price']}")
                print(f"PriceValidTill: {product['PriceValidTill']}")
                print(f"URL: {product['URL']}")
                print("---")
                
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Ensure log directory exists
    Path('logs').mkdir(exist_ok=True)
    
    # Run the scraper
    asyncio.run(main()) 