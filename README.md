# PriceTracker

## About the Project
PriceTracker is a Django application designed to collect and manage product information from registered URLs. It performs web scraping to extract product prices and promotions, storing the data in a history log for monitoring purposes.

## Features
- Store and manage product URLs.
- Automatically scrape product data and prices.
- Maintain a historical log of prices and promotions.
- Django Admin interface for data visualization and management.
- Custom Django command (`getprices`) to fetch and update prices.

## Technologies Used
- Django – Backend framework.
- Requests & BeautifulSoup – Web scraping tools.
- SQLite/PostgreSQL – Database management.
- Virtual Environment (venv) – Dependency management.

## Installation and Setup
### Prerequisites
- Python 3 installed on your system.
- Virtual environment set up for dependency isolation.

### Steps to Run the Project
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a Django superuser (for admin access)
python3 manage.py createsuperuser

# Run database migrations
python3 manage.py migrate

# Execute the scraping command to fetch product data
python3 manage.py getprices
```

## Admin Panel
After running the setup, you can access the Django Admin interface to view and manage stored data.

1. Start the Django development server:
   ```bash
   python3 manage.py runserver
   ```
2. Open your browser and go to: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
3. Log in using the superuser credentials created earlier.

## How It Works
- The `getprices` command iterates through all registered URLs in the database.
- It makes HTTP requests to each URL and extracts product data.
- Products are stored using the `data-product-sku` attribute as their unique identifier.
- A history record is created for each product, logging prices and promotional status.


