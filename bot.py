## This bot is meant to collect watch hours not to collect rewards.
## The bot will inject the session cookies from a set user and refresh the stream every 15 minutes.
## The selenium packager is compatible with multiple browser.
## This script is provided for education purpose only and all liabilities are waved. 
## Use at your own risk.

# Packages
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.firefox.options import Options # type: ignore
import time
import datetime
import json
import sys

# Checks for correct arguments
if len(sys.argv) != 3:
    print("Usage: python3 start_bot.py <twitch_channel> <cookies_file>\n")
    print("<twitch_channel> must be a Twitch channel")
    print("<cookies_file>   must be a .json file\n")
    sys.exit(1)
else:
    cookies_file = sys.argv[2]
    # Checks if the file is .json
    try:
        with open(cookies_file) as file:
            file_data = file.read()
            cookies = json.loads(file_data)
    except:
        print("\nError: File submited not a .json")
        print("\nExiting...\n")
        sys.exit(1)
    
    print(f"\nImporting cookies from: {cookies_file}\n")

# Variables
twitch = "https://twitch.tv/"
channel = sys.argv[1]
twitch_channel = twitch + channel 
refresh_count = 0
offline_hours = 0

# Browser Settings
options = Options()
options.add_argument("-headless") # Comment to see the Firefox GUI in action

# Functions
def get_time():
    current_time = datetime.datetime.now().time()
    return str(current_time)

def is_live():
    try:
        options.add_argument("-headless")
        with webdriver.Firefox(options=options) as checker:
            checker.get(twitch_channel)
            time.sleep(10)
            live_badge = checker.find_element(By.CLASS_NAME, "live-time")
            if live_badge:
                return True
    except:
        return False

def banner_bypass():
    # Tries to bypass the 'content is intended for certain audiences' banner
    try:
        driver.find_element(By.XPATH, "//button[@data-a-target='content-classification-gate-overlay-start-watching-button']").click()
        print("\nGot through the access banner.")
    except:
        print("\nNo banner appeared. Skipping button press.")
    finally:
        print("\n" + get_time() + " | Session Started")
        print("Current Page: " + driver.title + " (" + driver.current_url +")")


# Runing the Bot
with webdriver.Firefox(options=options) as driver:
    driver.get(twitch)

    # Cookie Injection
    for cookie in cookies:
        try:
            print("Injecting Cookies:", cookie["name"])
            driver.add_cookie(cookie)
        except:
            print("Failed to Inject:", cookie["name"])

    if is_live():
        # Loads page with session
        time.sleep(10) 
        driver.get(twitch_channel)
        # Waits for banner to load
        time.sleep(15) 
        banner_bypass()

    # Loop for refreshing the browser every 15 minutes
    while True:
        # Checks if still live
        while not is_live():
            if offline_hours == 0:
                print("\n====================================================================")

            print("Streamer is offline (" + str(offline_hours) + " hours total).")
            print("Checking again in 60 minutes. Current time:", get_time())

            if offline_hours != 0 and refresh_count != 0:
                refresh_count = 0 # Set refesh count back to 0 if streamer went offline
            elif offline_hours == 0 and refresh_count == 0 and driver.title != "Twitch":
                driver.get(twitch) # Bot stays out of chat if channel is offline ###### Possible to add a list of stream options - if 1st not avail check 2nd  then 3rd ...
                print("Changing Page: " + driver.title + " (" + driver.current_url +")")

            time.sleep(3600) # Waits for 60 minutes
            offline_hours += 1

        if offline_hours == 0:
            time.sleep(900)
            refresh_count += 1
        else: 
            driver.get(twitch_channel)
            banner_bypass()
            
        offline_hours = 0

        if refresh_count != 0:
            print(get_time() + " | Refreshed " + str(refresh_count) + " times, totalling " + str(refresh_count*15) + " minutes of watch time (" + str(refresh_count/4) + " hours).")
        else:
            print("\n====================================================================")
            print(get_time() + " | Starting Watch Time.")
            banner_bypass()
