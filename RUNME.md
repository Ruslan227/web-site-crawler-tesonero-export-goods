## Install Pipenv (if not installed)
```
pip install pipenv
```

## Install dependencies
```
pipenv install
```

## Install Playwright browsers
```
pipenv run playwright install chromium
```

## Configure environment
### Copy the secrets template:
```
cp secrets.env.template secrets.env
```
### Edit secrets.env with your configuration:
```
BASE_URL="https://some.site"
PRODUCT_TYPE1_TAB_NAME="type1"
PRODUCT_TYPE2_TAB_NAME="type2"
# OUTPUT_FILE="custom_filename.xlsx"  # Optional override
```

## Run the scraper
```
pipenv run python3 scraper.py
```