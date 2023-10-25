import logging
import os

# ENVIRONMENT VARIABLES
ALPHA_URL = os.environ.get('ALPHA_URL', 'https://www.alphavantage.co/')
ALPHA_API_KEY = os.environ.get('ALPHA_API_KEY', 'X86NOH6II01P7R24')
DB_URL = os.environ.get('DB_URL', 'sqlite:///./database.db')
LOGGER = logging.getLogger('hexagonal')
