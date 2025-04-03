from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
import os
import requests
import json
load_dotenv()

base_url = "https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1"
webhook_url = os.getenv("webhook_url")
key = os.getenv("key")
country_code = os.getenv("country_code")

with open("src/devices.json", "r") as f:
    devices = json.load(f)
    webhookContent = ""
    for device in devices:
        status_changed = False
        package_id = device["packageId"]
        querystring = {
            "key": key, "packageId": package_id, "country_code": country_code
        }
        response = requests.get(base_url, params=querystring)
        response_json = response.json()

        if response_json["response"]["inventory_available"] != device["available"]:
            device["available"] = response_json["response"]["inventory_available"]
            status_changed = True

        if status_changed:
            with open("src/devices.json", "w") as f:
                json.dump(devices, f, indent=2)
            webhookContent += f"{device['capacity']} {"OLED " if device['OLED'] else "LCD"} {"is available" if device['available'] else "is not available"}\n"
    if webhookContent != "":
        webhook = DiscordWebhook(
            url=webhook_url, 
            content=webhookContent
        )
        webhook.execute()