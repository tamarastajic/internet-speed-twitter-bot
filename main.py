from InternetSpeedTwitterBot import InternetSpeedTwitterBot

# ~~~~ INTERNET SPEEDS PROMISED IN THE CONTRACT AND MARGINAL ERROR CONSIDERED BEFORE COMPLAINING ~~~~
PROMISED_DOWN = 600
PROMISED_UP = 60
MARGINAL_ERROR = 20

# ~~~~ TWITTER CREDENTIALS ~~~~
# Input your own
TWITTER_EMAIL = YOUR_TWITTER_EMAIL
TWITTER_PASSWORD = YOUR_TWITTER_PASSWORD
TWITTER_USERNAME = YOUR_TWITTER_USERNAME

# Create an InternetSpeedTwitterBot based on different parameters
bot = InternetSpeedTwitterBot(PROMISED_DOWN, PROMISED_UP, MARGINAL_ERROR,
                              TWITTER_EMAIL, TWITTER_PASSWORD, TWITTER_USERNAME)

bot.acquire_internet_speed()


