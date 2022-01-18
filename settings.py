from dotenv import load_dotenv
import os
import logging

# Ingurune-aldagaiak zamatu, .env fitxategirik badago
load_dotenv()

# Herokun edo lokalean ari garen jakiteko

HEROKU = os.environ.get('HEROKU')

# Telegram bot TOKEN and my user
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Set the port number to listen in for the webhook
PORT = int(os.environ.get('PORT', 8443))

# Enable loggingencrypted
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)