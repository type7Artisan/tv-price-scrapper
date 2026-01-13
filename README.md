# TV Price Scraper

A Python-based web scraper that collects TV prices from various Canadian retailers.

## Prerequisites

- Python 3.8 or higher
- Git (optional)

## Installation

### Windows

1.  Download and extract the ZIP file

2.  Open Command Prompt and navigate to the project directory:
    cd path\to\project

3.  Create a virtual environment:
    python -m venv venv

4.  Activate the virtual environment:
    venv\Scripts\activate

5.  Install required packages:
    pip install -r requirements.txt

### macOS/Linux

1. Download and extract the ZIP file:

2. Open Terminal and navigate to the project directory:
   cd path/to/project

3. Create a virtual environment:
   python3 -m venv venv

4. Activate the virtual environment:
   source venv/bin/activate

5. Install required packages:
   pip install -r requirements.txt

## Project Structure

project/
├── data/
│ ├── cache/ # Cached results
│ └── results/ # Scraped results (e.g., visions_prices_20250327_171622.json)
├── logs/ # Log files
├── scrapers/  
│ ├── **init**.py
│ ├── amazon_scraper.py
│ ├── bestbuy_scraper.py
│ ├── canadiantire_scraper.py
│ ├── costco_scraper.py
│ ├── dufresne_scraper.py
│ ├── lg_scraper.py
│ ├── londondrugs_scraper.py
│ ├── samsung_scraper.py
│ ├── staples_scraper.py
│ ├── tanguay_scraper.py
│ ├── teppermans_scraper.py
│ └── visions_scraper.py
├── .env # Environment variables (if needed)
├── CHANGELOG.md # Project changes history
├── main.py # Main script
├── price_scraper.py # Price scraper implementation
├── products.json # Sample product list
├── requirements.txt # Package dependencies
└── README.md # This file

## Usage

1. Ensure your virtual environment is activated (you should see `(venv)` in your terminal)

2. Run the scraper:
   python main.py

3. Choose your input method when prompted:
   - Option 1: Enter a single product name
   - Option 2: Use a JSON file with multiple products

### Using a JSON File

Create a `products.json` file with your products:
[
{ "name": "Samsung 65\" 4K Tizen Smart QLED TV - QN65Q60DAFXZC" },
{ "name": "LG 55\" QNED80 4K Smart QLED TV - 55QNED80TUC" },
{ "name": "Hisense 50\" 4K Smart Google AI Upscaler LED TV - 50A68N" }
]

## Available Retailers

- Visions
- Canadian Tire
- Costco
- Best Buy
- Amazon
- London Drugs
- Dufresne
- Tanguay
- Teppermans
- LG
- Samsung
- Staples

## Required Packages

All required packages are listed in requirements.txt:

- aiohttp>=3.8.0 (async HTTP client)
- beautifulsoup4>=4.9.3 (HTML parsing)
- lxml>=4.9.0 (XML/HTML parser)
- python-dotenv>=0.19.0 (environment variables)
- requests>=2.26.0 (HTTP library)

Note: asyncio, typing, and pathlib are built-in Python modules and don't need to be installed.

## Results

Results are saved in two locations:

1. Console output showing:
   - Brand
   - Website
   - Title
   - Price
   - URL
2. JSON files in `data/results/` directory with timestamp (e.g., visions_prices_20250327_171622.json)

## Troubleshooting

1. If you get import errors:
   pip install -r requirements.txt

2. If you get permission errors creating directories:

   - Windows: Run Command Prompt as Administrator
   - Mac/Linux: Use `sudo` or check folder permissions

3. If a scraper fails:
   - Check your internet connection
   - Verify the product name/model number
   - Check if the retailer's website is accessible

## Features

- **Async/Await Support**: Uses Python's asyncio for concurrent scraping
- **Caching System**: Reduces redundant requests with configurable cache duration
- **Rate Limiting**: Prevents IP blocking with built-in rate limiting
- **Error Handling**: Comprehensive error handling and logging
- **Multiple Retailers**: Support for 12+ Canadian retailers
- **Flexible Input**: Support for single products or batch processing via JSON
- **Structured Output**: Results saved in JSON format with timestamps

## Current Status

- **Visions**: Fully functional and tested
- **Other Retailers**: Framework implemented, may require additional configuration for anti-scraping measures

## Notes

- Some retailers may block automated requests due to anti-scraping measures
- Prices and availability may vary by location
- Cache results are stored for 1 hour (configurable)
- All times are in local timezone
- Make sure to create the following directories if they don't exist:
  ```bash
  mkdir -p data/cache data/results logs
  ```

## Technical Stack

- **Python 3.8+**
- **Async Programming**: asyncio, aiohttp
- **Web Scraping**: BeautifulSoup4, lxml
- **Architecture**: Object-oriented design with base classes and inheritance
