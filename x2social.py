import os
import time
import logging
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
from selenium.common.exceptions import NoSuchElementException

# ==== CONFIGURATION ====
TWITTER_URL = 'https://x.com/ghazayel'
TELEGRAM_URL = 'https://web.telegram.org/k/#@ghazayel'
FACEBOOK_URL = 'https://www.facebook.com/messages/t/###/'
HISTORY_FILE = 'tweet_history.txt'

# ==== LOGGING SETUP ====
logging.basicConfig(
    filename='x2social.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("🚀 Starting browsers")
logging.info("🚀 Starting browsers")

# ==== TELEGRAM (Edge) ====
edge_options = EdgeOptions()
edge_options.add_argument(r'user-data-dir=C:\Users\ghazayel\AppData\Local\Microsoft\Edge\User Data')
edge_options.add_argument('--profile-directory=Profile 1')
telegram_driver = webdriver.Edge(service=EdgeService('C:/edgedriver/msedgedriver.exe'), options=edge_options)
telegram_driver.get(TELEGRAM_URL)

# ==== WHATSAPP (Chrome) ====
chrome_options_whatsapp = ChromeOptions()
whatsapp_profile = r"C:\Automation\ChromeUser\whatsapp_profile"
os.makedirs(whatsapp_profile, exist_ok=True)
chrome_options_whatsapp.add_argument(f"user-data-dir={whatsapp_profile}")
chrome_options_whatsapp.add_argument("--disable-blink-features=AutomationControlled")
chrome_options_whatsapp.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options_whatsapp.add_experimental_option("useAutomationExtension", False)
chrome_options_whatsapp.add_argument("--password-store=basic")
whatsapp_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options_whatsapp)
whatsapp_driver.get('https://web.whatsapp.com')

# ==== TWITTER (Chrome) ====
chrome_options_twitter = ChromeOptions()
twitter_profile = r"C:\Automation\ChromeUser\twitter_profile"
os.makedirs(twitter_profile, exist_ok=True)
chrome_options_twitter.add_argument(f"user-data-dir={twitter_profile}")
chrome_options_twitter.add_argument("--disable-blink-features=AutomationControlled")
chrome_options_twitter.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options_twitter.add_experimental_option("useAutomationExtension", False)
chrome_options_twitter.add_argument("--password-store=basic")
twitter_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options_twitter)
twitter_driver.get(TWITTER_URL)

# ==== FACEBOOK (Chrome) ====
chrome_options_facebook = ChromeOptions()
facebook_profile = r"C:\Automation\ChromeUser\facebook_profile"
os.makedirs(facebook_profile, exist_ok=True)
chrome_options_facebook.add_argument(f"user-data-dir={facebook_profile}")
chrome_options_facebook.add_argument("--disable-blink-features=AutomationControlled")
chrome_options_facebook.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options_facebook.add_experimental_option("useAutomationExtension", False)
chrome_options_facebook.add_argument("--password-store=basic")
facebook_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options_facebook)
facebook_driver.get(FACEBOOK_URL)

# ==== LOAD TWEET HISTORY ====
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        tweet_history = set(f.read().splitlines())
else:
    tweet_history = set()

# ==== UTILITY FUNCTIONS ====

def remove_non_bmp(text):
    removed = [c for c in text if ord(c) > 0xFFFF]
    if removed:
        log_msg = f"🛑 Removed non-BMP characters: {''.join(removed)} (e.g. U+{ord(removed[0]):04X})"
        print(log_msg)
        logging.info(log_msg)
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def save_to_history(tweet):
    tweet_history.add(tweet)
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(tweet + '\n')

def clean_tweet_telegram(tweet):
    cleaned = tweet.strip()
    return f"🔴 {cleaned}"

def clean_tweet_social(tweet):
    cleaned = tweet.strip().replace("#", "").replace("_", " ")
    return cleaned

def get_latest_tweet():
    twitter_driver.switch_to.window(twitter_driver.current_window_handle)
    twitter_driver.refresh()
    time.sleep(5)
    try:
        tweet = WebDriverWait(twitter_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article div[lang]'))
        ).text
        return tweet
    except Exception as e:
        logging.error(f"❌ Error fetching tweet: {e}")
        twitter_driver.save_screenshot("error_tweet.png")
        return None

def send_to_whatsapp(message):
    logging.info("📤 Sending to WhatsApp...")
    try:
        whatsapp_driver.switch_to.window(whatsapp_driver.current_window_handle)
        cleaned = remove_non_bmp(message)
        box = WebDriverWait(whatsapp_driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
        box.send_keys(cleaned)
        box.send_keys(Keys.RETURN)
        logging.info("✅ WhatsApp message sent")
    except Exception as e:
        logging.error(f"❌ WhatsApp send failed: {e}")
        whatsapp_driver.save_screenshot("wa_error.png")

def send_to_telegram(message):
    logging.info("📤 Sending to Telegram...")
    try:
        telegram_driver.switch_to.window(telegram_driver.window_handles[0])
        WebDriverWait(telegram_driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Broadcast"]'))
        )
        try:
            box = telegram_driver.find_element(By.XPATH, '//span[text()="Broadcast"]/ancestor::div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')
        except NoSuchElementException:
            box = telegram_driver.find_element(By.XPATH, '//div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')
        telegram_driver.execute_script("arguments[0].innerText = arguments[1];", box, message)
        box.send_keys(Keys.ENTER)
        logging.info("✅ Telegram message sent")
    except Exception as e:
        logging.error(f"❌ Telegram send failed: {e}")
        telegram_driver.save_screenshot("tg_error.png")

def send_to_facebook(message):
    logging.info("📤 Sending to Facebook Messenger...")
    try:
        facebook_driver.switch_to.window(facebook_driver.current_window_handle)
        box = WebDriverWait(facebook_driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Aa" and @role="textbox"]'))
        )
        box.click()
        time.sleep(1)
        box.send_keys(Keys.SPACE)
        box.send_keys(Keys.BACKSPACE)
        box.send_keys(message)
        box.send_keys(Keys.ENTER)
        logging.info("✅ Facebook message sent")
        print("[✓] Message sent to Facebook.")
    except Exception as e:
        logging.error(f"❌ Facebook send failed: {e}")
        print("[✗] Failed to send to Facebook:", str(e))
        facebook_driver.save_screenshot("fb_error.png")

# ==== MAIN LOOP ====
print("🟢 Monitoring started")
logging.info("🟢 Monitoring started")

while True:
    print("⏳ Checking for new tweets...")
    logging.info("⏳ Checking for new tweets...")
    tweet = get_latest_tweet()
    if tweet and tweet not in tweet_history:
        print(f"🆕 New tweet found: {tweet}")
        logging.info(f"🆕 New tweet found: {tweet}")
        # Prepare platform-specific messages
        msg_telegram = clean_tweet_telegram(tweet)
        msg_social = clean_tweet_social(tweet)
        # Dispatch
        send_to_whatsapp(msg_social)
        send_to_telegram(msg_telegram)
        send_to_facebook(msg_social)
        save_to_history(tweet)
    else:
        print("🔁 No new tweet.")
        logging.info("🔁 No new tweet.")
    time.sleep(60)
