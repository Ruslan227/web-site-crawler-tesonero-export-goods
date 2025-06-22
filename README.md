# 📦 Web-site Scraper 🕷️

A web scraper that extracts product data from a **JavaScript-rendered SPA (Single Page Application)**. This project demonstrates professional web scraping techniques with robust error handling, configuration management, and data export capabilities.

## ⚡ Key Challenge: SPA Handling
The target website is a **JavaScript-rendered Single Page Application** where:
- Initial HTML response contains minimal content
- Product data is loaded dynamically via JavaScript
- Navigation occurs without page reloads
- Content rendering depends on client-side execution

## ✨ Key Features
- **SPA Automation** - Handles JavaScript-rendered content with browser automation
- **Multi-level scraping** - Extracts category listings and detailed product information
- **Playwright integration** - Automates modern JavaScript-heavy websites
- **Professional error handling** - Comprehensive logging and error recovery
- **Smart throttling** - Random delays to avoid detection
- **Secrets management** - Secure configuration handling
- **Excel export** - Clean data output in spreadsheet format

## 🧰 Tech Stack
| Component | Technology | SPA Handling |
|-----------|------------|--------------|
| **Core Language** | Python 3.9+ | - |
| **Browser Automation** | Playwright | Executes JS, waits for network idle |
| **DOM Interaction** | Playwright Selectors | Handles dynamic element loading |
| **Tab Management** | Playwright Page API | Simulates user interactions |
| **Data Processing** | Pandas | - |
| **Configuration** | python-dotenv | - |
| **Dependency Mgmt** | Pipenv | - |
| **Logging** | Python logging | - |

## 📊 Scraped Data Points
- Product names and descriptions
- Pricing information
- SKU and stock availability
- Material composition
- Product dimensions
- Detailed characteristics
- Category hierarchies

## 🛡️ Robustness Features for SPAs
- **Dynamic content waiting** - Smart waits for network idle and element visibility
- **Tab switching logic** - Simulates user clicks with state validation
- **JavaScript execution** - Runs in-page scripts to trigger content loading
- **Fallback extraction** - Multiple content retrieval strategies
- **DOM state validation** - Checks for content presence before extraction
- **Comprehensive error logging** - Detailed error context for troubleshooting

## 📂 Project Structure
/

├── 🕷️ scraper.py - Main scraping script with SPA handling logic

├── 🔒 secrets_utils.py - Secure configuration loader for secrets management

├── 📝 Pipfile - Dependency manifest for Pipenv

├── 🔐 Pipfile.lock - Locked dependency versions for reproducibility

├── 📖 README.md - Project documentation and technical overview

├── ▶️ RUNME.md - Step-by-step execution instructions

├── 🔑 secrets.example - Configuration template (rename to secrets.env)

└── 🚫 .gitignore - Patterns to exclude from version control