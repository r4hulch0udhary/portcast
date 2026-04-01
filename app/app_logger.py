import logging
import os
from app.config import config

def setup_logging():
    """Set up logging configuration."""
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(
        filename='log/app.log',
        level=logging.DEBUG if config.debug else logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )