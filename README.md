# RefurbDeck Stock Checker

This project is a Python-based tool to monitor the availability of refurbished Steam Deck devices. It checks the stock status of specific device configurations and sends notifications via Discord when availability changes.

## Features

- Monitors stock availability for different Steam Deck configurations.
- Sends Discord notifications when stock status changes.
- Configurable via environment variables.
- Docker support for easy deployment.

## Prerequisites

- Python 3.7 or higher (if not using Docker)
- A Discord webhook URL
- Steam API key from https://steamcommunity.com/dev/apikey
- `dotenv` and `discord_webhook` Python packages (if not using Docker)

## Installation

### Using Python

1. Clone the repository:

   ```bash
   git clone https://github.com/coreyg142/RefurbDeckStockChecker.git
   cd RefurbDeckStockChecker
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:

   ```
   webhook_url=YOUR_DISCORD_WEBHOOK_URL
   key=YOUR_STEAM_API_KEY
   country_code=YOUR_COUNTRY_CODE
   check_interval=TIME_IN_SECONDS # Optional, defaults to 60
   ```

4. Update `config/devices.json` with the configurations you want to monitor.

### Using Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/coreyg142/RefurbDeckStockChecker.git
   cd RefurbDeckStockChecker
   ```

2. Build the Docker image:

   ```bash
   docker build -t refurbdeck-stock-checker .
   ```

3. Docker compose:

   ```yaml
   app:
     image: refurbdeck-stock-checker:latest
     container_name: refurbdeck-stock-checker
     environment:
       - key=YOUR_STEAM_API_KEY
       - country_code=YOUR_COUNTRY_CODE
       - webhook_url=YOUR_DISCORD_WEBHOOK_URL
       - check_interval=60 # Optional, defaults to 60 seconds
       - TZ=America/New_York # Optional
     volumes:
       - PATH_TO_CONFIG/config:/usr/app/config
   ```

   Ensure the `config` directory contains your `devices.json` file.

## Usage

### Using Python

Run the script to check stock availability:

```bash
python src/script.py
```

The script will:

- Query the Steam API for the availability of each device in `config/devices.json`.
- Update the `available` status in `config/devices.json`.
- Send a Discord notification if the availability status changes.

### Using Docker

The Docker container will automatically run the script and check availability at the configured interval.

## Example Output

A Discord notification might look like this:

```
512GB OLED is available
1TB OLED is not available
```
