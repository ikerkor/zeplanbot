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

# Ekintza mota emojiak
dicMotaEmoji = {'Haur jarduera': '\U0001F476',
                'Kontzertua': '\U0001F3B6',
                'Antzerkia': '\U0001F3AD',
                'Bertsolaritza': '\U0001F3A4',
                'Hitzaldia': '\U0001F5E9',
                'Erakusketa': '\U0001F5BC',
                'Ikus-entzunezko emanaldia': '\U0001F3AC',
                'Dantza': '\U0001F483',
                'Formakuntza': '\U0001F9D1\U0000200D\U0001F3EB',
                'Ekitaldiak/jardunaldiak': '\U0001F5EB'}
