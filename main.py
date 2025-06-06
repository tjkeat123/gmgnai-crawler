from seleniumbase import Driver
from selenium.webdriver.common.by import By

import base58

import time
import pandas as pd

token_address = input("Enter the token address: ")
base58_token_address = base58.b58decode(token_address)

num_traders = int(input("Enter the number of traders to get: "))

if_full_address = input("""Do you want to get the full address for fund sources? (y/n): 
                        (y): 52CcwUJYPsnZVN3w8zLztafBB2BV7YLc2rPsfic6izqH
                        (n): 52Ccw...zqH / Binance / MEXC
                        """)

if if_full_address == "y":
    full_address = True
else:
    full_address = False

if token_address == "":
    print("Token address is required")
    exit()
elif len(base58_token_address) != 32: # Solana addresses are 32 bytes
    print("Invalid token address")
    exit()

website_url = "https://gmgn.ai/sol/token/" + token_address

driver = Driver(uc=True, headless=False)

driver.uc_open_with_reconnect(website_url, reconnect_time=6) # open the website with a 6 second reconnect timeout

driver.uc_gui_click_captcha() # solve cloudflare captcha when there is one

time.sleep(5) # gmgn is slow to load, wait to make sure the page is loaded

driver.implicitly_wait(10) # set the timeout for every element to 10 seconds

# close the popup login window
close_icon = driver.find_element(
    By.XPATH,
    "//*[name()='path' and @fill-rule='evenodd' and starts-with(@d,'M2.29111')]"
)
close_icon.click()

# close the introductory popup
for i in range(7):
    next_button = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Next')]"
    )
    next_button.click()

finish_button = driver.find_element(
    By.XPATH,
    "//*[contains(text(), 'Finish')]"
)
finish_button.click()

# move to the tab where it shows the top traders
trader_tab = driver.find_element(
    By.ID,
    "traders"
)
trader_tab.click()

addresses = []
balances = []
sources = []
pnls = []
pnl_pcts = []

# for each row of the top 10 traders
for i in range(num_traders):
    # get the entire row
    row = driver.find_element(
        By.CSS_SELECTOR,
        f'div[row-index="{i}"]'
    )

    # get the address
    address = row.get_attribute("row-id").split("_")[0]
    addresses.append(address)
    
    # get the balance
    balance = row.find_element(
        By.CSS_SELECTOR,
        'div[col-id="balance"]'
    )
    balance_text = balance.find_element(
        By.CSS_SELECTOR,
        'div div'
    )
    balances.append(balance_text.text.split('\n')[0])

    # get the source of funds for the wallet
    source = row.find_element(
            By.CSS_SELECTOR,
            'div[col-id="source"]'
        )
    if not full_address:
        source_text = source.find_element(
            By.CSS_SELECTOR,
            'div div div a div div' 
        )
        sources.append(source_text.text)
    else:
        source_text = source.find_element(
            By.CSS_SELECTOR,
            'div div div a'
        )
        source_href = source_text.get_attribute("href").split("/")[-1]
        sources.append(source_href)

    # get the pnl
    pnl = row.find_element(
        By.CSS_SELECTOR,
        'div[col-id="pnl"]'
    )
    pnl_text = pnl.find_element(
        By.CSS_SELECTOR,
        'div span:nth-child(1)'
    )
    pnl_pct_text = pnl.find_element(
        By.CSS_SELECTOR,
        'div span:nth-child(2)'
    )
    pnls.append(pnl_text.text)
    pnl_pcts.append(pnl_pct_text.text)

# put the data into a dataframe then into a csv file
df = pd.DataFrame(
    {
        "Address": addresses,
        "Balance": balances,
        "Source": sources,
        "PnL": pnls,
        "PnL %": pnl_pcts
    }
)

df.to_csv("top_traders_" + token_address + ".csv", index=False)
print("Saved to top_traders_" + token_address + ".csv")

driver.quit()