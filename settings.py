import os
import logging

from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s | %(levelname)-7s | %(name)-30s [%(lineno)4d] - %(message)s",
    level=logging.INFO
)

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

print(f'{TOKEN=}')
