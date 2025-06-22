# 📦 Web-site Scraper 🕷️

A web scraper that extracts product data from e-commerce site. This project demonstrates professional web scraping techniques with robust error handling, configuration management, and data export capabilities.

## ✨ Key Features
- **Multi-level scraping** - Extracts category listings and detailed product information
- **Playwright integration** - Automates modern JavaScript-heavy websites
- **Professional error handling** - Comprehensive logging and error recovery
- **Smart throttling** - Random delays to avoid detection
- **Secrets management** - Secure configuration handling
- **Excel export** - Clean data output in spreadsheet format

## 🧰 Tech Stack
| Component | Technology |
|-----------|------------|
| **Core Language** | Python 3.9+ |
| **Browser Automation** | Playwright |
| **Data Processing** | Pandas |
| **Configuration** | python-dotenv |
| **Dependency Mgmt** | Pipenv |
| **Logging** | Python logging |

## 📊 Scraped Data Points
- Product names and descriptions
- Pricing information
- SKU and stock availability
- Material composition
- Product dimensions
- Detailed characteristics
- Category hierarchies

## 🛡️ Robustness Features
- Dynamic content handling
- Tab switching logic with fallbacks
- CSS selector redundancy
- Page state validation
- Screenshot-based debugging
- Comprehensive error logging

## 📂 Project Structure
/
├── scraper.py # Main scraping logic
├── secrets_utils.py # Secure configuration loader
├── Pipfile # Dependency manifest
├── Pipfile.lock # Locked dependencies
├── .gitignore # Ignore patterns
├── RUNME.md # Execution instructions
└── secrets.example # Configuration template