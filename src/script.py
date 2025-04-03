from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
import os
import requests
import json
import signal
import sys
import time
import logging
import traceback
load_dotenv()
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ],
    level=logging.INFO
)

def signal_handler(sig, frame):
    logger.info("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

logger.info("Starting script...")
logger.info("Loading environment variables...")
base_url = "https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1"
webhook_url = os.getenv("webhook_url")
key = os.getenv("key")
country_code = os.getenv("country_code")
check_interval = int(os.getenv("check_interval", 60))
send_webhooks = os.getenv("send_webhooks", "true").lower() == "true"

def send_webhook_message(message):
    if send_webhooks:
        webhook = DiscordWebhook(
            url=webhook_url, 
            content=message
        )
        webhook.execute()

def check_availability_device(device):
    status_changed = False
    package_id = device["packageId"]
    querystring = {
        "key": key, "packageId": package_id, "country_code": country_code
    }
    try:
        response = requests.get(base_url, params=querystring)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for package ID {package_id}: {e}")
        send_webhook_message(f"Error fetching data for package ID\n{e}")
        return
    response_json = response.json()

    if response_json["response"]["inventory_available"] != device["available"]:
        device["available"] = response_json["response"]["inventory_available"]
        status_changed = True

    return status_changed


def check_availability():
    logger.info("Checking availability...")
    if not webhook_url or not key or not country_code:
        logger.error("Missing required environment variables.")
        return
    try:
        with open("config/devices.json", "r") as f:
            devices = json.load(f)
        webhookContent = ""
        for device in devices:
            status_changed = check_availability_device(device)
            if status_changed:
                webhookContent += f"{device['capacity']} {"OLED" if device['OLED'] else "LCD"} {"is available" if device['available'] else "is not available"}\n"
                with open("config/devices.json", "w") as f:
                    json.dump(devices, f, indent=2)

        if webhookContent != "":
            logger.info(webhookContent)
            send_webhook_message(webhookContent)
        else:
            logger.info("No changes in availability status.")
    except Exception as e:
        logger.error(f"Error running script: {traceback.format_exc()}")
        send_webhook_message(f"An error occurred while running the script.\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    check_availability()
    time.sleep(check_interval)  # Check every x seconds
    while True:
        check_availability()
        time.sleep(check_interval)  # Check every x seconds