
# 🚀 x2social
**x2social** is a Python-powered automation tool that monitors a specific Twitter account (currently [@ghazayel](https://x.com/ghazayel)) and instantly shares every new tweet to WhatsApp, Telegram, and Facebook Messenger using headless browser automation via Selenium.

---

## ✨ Features

- 🔁 **Real-time Tweet Monitoring**  
  Continuously monitors a Twitter page for new tweets.

- 💬 **Multi-Platform Broadcasting**  
  Instantly sends tweets to:
  - 📲 WhatsApp Web
  - 📢 Telegram Web
  - 💬 Facebook Messenger

- 🔒 **Session-Preserving User Profiles**  
  Uses saved Chrome/Edge user profiles to keep you logged in.

- 🧼 **Cleans Tweet Content**  
  Formats and sanitizes messages per platform, removing hashtags and emojis if needed.

- 📜 **Tweet History Tracking**  
  Prevents duplicate messages using a history log.

- 📸 **Error Screenshots**  
  Saves a screenshot whenever something goes wrong for easy debugging.

---

## 🛠️ Setup

### 1. 📦 Install Python Requirements

```bash
pip install selenium webdriver-manager
```

### 2. 🧭 Configure User Profiles

Ensure your browsers are already logged in to:
- WhatsApp Web
- Telegram Web
- Facebook Messenger

Update these paths in the code if needed:

```python
# Example (Windows paths)
telegram_profile = "C:\\Users\\<you>\\AppData\\Local\\Microsoft\\Edge\\User Data"
whatsapp_profile = "C:\\Automation\\ChromeUser\\whatsapp_profile"
twitter_profile = "C:\\Automation\\ChromeUser\\twitter_profile"
facebook_profile = "C:\\Automation\\ChromeUser\\facebook_profile"
```

### 3. 🧪 Run the Script

```bash
python x2social.py
```

---

## 📁 File Structure

```text
├── x2social.py          # Main script
├── tweet_history.txt    # Stores previously shared tweets
├── x2social.log         # Log file for monitoring
├── wa_error.png         # WhatsApp error screenshot
├── tg_error.png         # Telegram error screenshot
├── fb_error.png         # Facebook error screenshot
```

---

## 📸 Demo

> *Coming soon!* A short video showcasing the real-time automation flow from X to social platforms.

---

## 🧠 How It Works

1. **Launches 4 browser instances** (X, WhatsApp, Telegram, Facebook) using Selenium.
2. **Checks for a new tweet** every 60 seconds.
3. **Formats and sends** the tweet to each platform with custom formatting:
   - Telegram gets 🔴 prefixed messages.
   - WhatsApp and Facebook get cleaned, hashtag-free versions.
4. **Updates the history file** to prevent re-sending the same tweet.

---

## ⚠️ Requirements & Notes

- **Browser drivers** (Edge & Chrome) are managed via `webdriver-manager`.
- Edge requires a **custom profile directory**; ensure you edit the script to your local paths.
- Sessions are kept using `user-data-dir`, so **login once manually**, then the session is reused.

---

## 💡 Future Ideas

- ✅ Auto-login detection & recovery
- 🌐 GUI frontend
- 📨 Support for more platforms (Discord, Slack, etc.)
- 🐍 Packaged as a PyPI module

---

## 🙏 Acknowledgments

- [Selenium WebDriver](https://www.selenium.dev/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- The open internet and coffee ☕️

---

## 🛡️ License

MIT License — use responsibly, and give a ⭐ if it helps you!

---

## 📫 Feedback

Feel free to open an issue or reach out if you'd like to improve or customize this tool further.

---

**Let the tweets fly!** 🕊️
