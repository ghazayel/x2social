import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ==== CONFIGURATION ====
TWITTER_URL = 'https://x.com/20fourLive'
TELEGRAM_URL = 'https://web.telegram.org/k/#@twentyfour_media'

# Files to track history
history_file = 'tweet_history.txt'

# ==== BROWSER SETUP ====
print("🚀 Starting browsers")

# Telegram (Edge)
edge_options = EdgeOptions()
edge_options.add_argument(r'user-data-dir=C:\Users\ghazayel\AppData\Local\Microsoft\Edge\User Data')
edge_options.add_argument('--profile-directory=Profile 1')
telegram_driver = webdriver.Edge(service=EdgeService('C:/edgedriver/msedgedriver.exe'), options=edge_options)
telegram_driver.get(TELEGRAM_URL)

# WhatsApp (Chrome)
chrome_options = ChromeOptions()
chrome_options.add_argument(r'user-data-dir=C:\Users\ghazayel\AppData\Local\Google\Chrome\User Data')
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--password-store=basic')
whatsapp_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Load tweet history
if os.path.exists(history_file):
    with open(history_file, 'r', encoding='utf-8') as f:
        tweet_history = set(f.read().splitlines())
else:
    tweet_history = set()

# ==== UTILITY FUNCTIONS ====
def save_to_history(tweet):
    tweet_history.add(tweet)
    with open(history_file, 'a', encoding='utf-8') as f:
        f.write(tweet + '\n')

def clean_tweet(tweet):
    return f"🔴 {tweet.strip()}"

def get_latest_tweet():
    twitter_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    twitter_driver.get(TWITTER_URL)
    try:
        tweet = WebDriverWait(twitter_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article div[lang]'))
        ).text
        twitter_driver.quit()
        return tweet
    except Exception as e:
        print(f"❌ Error fetching tweet: {e}")
        twitter_driver.save_screenshot("error_tweet.png")
        twitter_driver.quit()
        return None

def send_to_whatsapp(message):
    print("📤 Sending to WhatsApp...")
    whatsapp_driver.switch_to.window(whatsapp_driver.window_handles[1])
    try:
        box = WebDriverWait(whatsapp_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
        box.send_keys(message)
        box.send_keys(Keys.RETURN)
        print("✅ WhatsApp message sent")
    except Exception as e:
        print(f"❌ WhatsApp send failed: {e}")
        whatsapp_driver.save_screenshot("wa_error.png")

def send_to_telegram(message):
    print("📤 Sending to Telegram...")
    telegram_driver.switch_to.window(telegram_driver.window_handles[0])
    try:
        WebDriverWait(telegram_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Broadcast"]'))
        )
        try:
            box = telegram_driver.find_element(By.XPATH, '//span[text()="Broadcast"]/ancestor::div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')
        except NoSuchElementException:
            box = telegram_driver.find_element(By.XPATH, '//div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')

        telegram_driver.execute_script("arguments[0].innerText = arguments[1];", box, message)
        box.send_keys(Keys.ENTER)
        print("✅ Telegram message sent")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        telegram_driver.save_screenshot("tg_error.png")

# ==== MAIN LOOP ====
print("🟢 Monitoring started")
while True:
    print("⏳ Checking for new tweets...")
    tweet = get_latest_tweet()
    if tweet and tweet not in tweet_history:
        print(f"🆕 New tweet found: {tweet}")
        clean = clean_tweet(tweet)
        send_to_whatsapp(clean)
        send_to_telegram(clean)
        save_to_history(tweet)
    else:
        print("🔁 No new tweet.")
    time.sleep(60)
