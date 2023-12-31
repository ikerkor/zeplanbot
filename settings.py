from dotenv import load_dotenv
import os
import logging

# Ingurune-aldagaiak zamatu, .env fitxategirik badago
load_dotenv()


##### Beharrezko ingurun aldagaiak

# Telegram bot TOKEN and my user
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
MY_TELEGRAM_USER = os.environ.get('MY_TELEGRAM_USER')

##### Webhook bidez egin nahi bada bete beharrezko ingurune aldagaiak

# Webhook bidez edo polling bidez ari garen jakiteko (bool, berez 0)
WEBHOOK = os.environ.get("WEBHOOK")

# Webhook url helbidea
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://zeplanbot.herokuapp.com/") # "https://zeplanbot.herokuapp.com/" Adibidea baino ez

# Set the port number to listen in for the webhook
PORT = int(os.environ.get('PORT', 8443))  # B4A-eko deploymentean ez da erabiltzen.


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ekintza mota emojiak
dicMotaEmoji = {'Haur jarduera': '\U0001F476',
                'Kontzertua': '\U0001F3B6',
                'Antzerkia': '\U0001F3AD',
                'Bertsolaritza': '\U0001F3A4',
                'Hitzaldia': '\U0001F4AC',
                'Erakusketa': '\U0001F5BC',
                'Ikus-entzunezko emanaldia': '\U0001F3AC',
                'Dantza': '\U0001F483',
                'Formakuntza': '\U0001F9D1\U0000200D\U0001F3EB',
                'Ekitaldiak/jardunaldiak': '\U0001F4AC',
                'Lehiaketa': '\U0001F3C6',
                'Jaialdia': '\U0001F389',
                'Jaiak': '\U0001F978',
                'Bestelakoa': '\U0001F381'}
