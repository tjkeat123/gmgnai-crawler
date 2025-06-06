# gmgnai-crawler

#### This is a school project.

A tool for extracting top trader data from gmgn.ai for Solana tokens. This crawler collects information about traders including wallet addresses, balances, fund sources, and profit/loss metrics.

#### This crawler is made for Windows, it should also works on Linux with Chrome installed, but it would not work on WSL.

## Prerequisite

- Python 3.6+
- Chrome browser installed
- Git

## Setup

#### Clone this repository:

Linux
``` bash
git clone https://github.com/tjkeat123/gmgnai-crawler.git
cd gmgnai-crawler/
```

Windows
``` powershell
git clone https://github.com/tjkeat123/gmgnai-crawler.git
cd .\gmgnai-crawler\
```

#### Install dependencies:

Linux
``` bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows
``` powershell
py -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
```

#### Running the script

Linux
``` bash
python3 main.py
```

Windows
``` powershell
py .\main.py
```

## Usage

When you run the script, you'll be prompted to:
1. Enter a Solana token address
2. Specify how many traders to retrieve
3. Choose whether to display full addresses for fund sources

Below is an example of the output

``` bash
Enter the token address: 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN
Enter the number of traders to get: 20
Do you want to get the full address for fund sources? (y/n): 
                        (y): 52CcwUJYPsnZVN3w8zLztafBB2BV7YLc2rPsfic6izqH
                        (n): 52Ccw...zqH / Binance / MEXC
                        y
Saved to top_traders_6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN.csv
```

A Chrome window should pop out with some random movements, it is completely normal, just let it run. The script automatically handles Cloudflare captchas and navigates through the site to collect data.

## Output

The script generates a CSV file named `top_traders_[TOKEN_ADDRESS].csv` containing:
- Wallet addresses
- Token balances
- Fund sources
- Profit/Loss values
- Profit/Loss percentages

Note: This tool is for light usage only. Please use responsibly and respect website terms of service. Check out https://docs.gmgn.ai/index/cooperation-api-data-crawling-ip-whitelist for data crawling terms.