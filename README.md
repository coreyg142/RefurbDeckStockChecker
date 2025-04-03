# RefurbDeck Stock Checker

This project is a Python-based tool to monitor the availability of refurbished Steam Deck devices. It checks the stock status of specific device configurations and sends notifications via Discord when availability changes.

## Features

- Monitors stock availability for different Steam Deck configurations.
- Sends Discord notifications when stock status changes.
- Configurable via environment variables.

## Prerequisites

- Python 3.7 or higher
- A Discord webhook URL
- Steam API key from `https://steamcommunity.com/dev/apikey`
- `dotenv` and `discord_webhook` Python packages

## Installation

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
   ```

4. Update `src/devices.json` with the configurations you want to monitor.

## Usage

Run the script to check stock availability:

```bash
python src/script.py
```

The script will:

- Query the Steam API for the availability of each device in `devices.json`.
- Update the `available` status in `devices.json`.
- Send a Discord notification if the availability status changes.

## Example Output

A Discord notification might look like this:

```
512GB OLED is available
1TB OLED is not available
```
