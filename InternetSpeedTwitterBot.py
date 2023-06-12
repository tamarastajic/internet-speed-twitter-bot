from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

class InternetSpeedTwitterBot:

    def __init__(self, p_download, p_upload, error, twitter_email, twitter_password, twitter_username):
        self.promised_download = p_download
        self.promised_upload = p_upload
        self.marginal_error = error

        self.email = twitter_email
        self.password = twitter_password
        self.username = twitter_username

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def acquire_internet_speed(self):
        """A function that acquires the current internet speed and proceedes to the next step based on it."""
        self.driver.get("https://www.speedtest.net/")

        # Start the speed test
        button = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        button.click()

        time.sleep(45)

        # Close an ad if it appears
        try:
            close_ad = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
            close_ad.click()
        except NoSuchElementException:
            pass

        # Acquire download and upload speeds
        self.download = float(self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
        self.upload = float(self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)

        # Calculate the difference between what was promised and what internet speed was found
        self.dif_download = round(self.promised_download - self.download)
        self.dif_upload = round(self.promised_upload - self.upload)
        # If this difference is over the marginal error - complain on Twitter
        if self.dif_download > self.marginal_error or self.dif_upload > self.marginal_error:
            self.complain()
        else:
            print("Current internet speed is adequate based on the marginal error allowed.")

    def complain(self):
        """A function that logs into twitter using given credentials and complains about the current internet speed."""
        self.driver.get("https://twitter.com/home")
        time.sleep(2)

        # Enter Email
        email_input = self.driver.find_element(By.CSS_SELECTOR, '.css-901oao input')
        email_input.send_keys(self.email)
        time.sleep(1)
        email_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # If needed - enter username to verify
        try:
            username_input = self.driver.find_element(By.CSS_SELECTOR, '.css-901oao input')
            username_input.send_keys(self.username)
            time.sleep(1)
            username_input.send_keys(Keys.ENTER)
            time.sleep(2)
        except NoSuchElementException:
            pass

        # Enter password
        password_input = self.driver.find_elements(By.CSS_SELECTOR, '.css-901oao input')[1]
        password_input.send_keys(self.password)
        time.sleep(1)
        password_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Compose a tweet
        compose_tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div')
        compose_tweet_button.click()

        write_tweet = self.driver.find_element(By.CLASS_NAME, 'public-DraftEditor-content' )
        write_tweet.send_keys(self.compose_tweet())
        time.sleep(1)

        tweet_button = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButton"]')
        tweet_button.click()
        time.sleep(1)

        print("Tweet Posted.")


    def compose_tweet(self):
        """A function that composes a tweet based on whether the download or upload (or both) are under what was promised (based on the marginal error provided)"""
        tweet = "Hello internet provider! "
        if self.dif_download > self.marginal_error and self.dif_upload > self.marginal_error:
            tweet += f"My download speed is currently {self.dif_download}Mbps lower than the promised {self.promised_download}Mbps. " \
                     f"Furthermore, my upload speed is {self.dif_upload}Mbps lower than the promised {self.promised_upload}Mbps."
        elif self.dif_download > self.marginal_error:
            tweet += f"My download speed is currently {self.dif_download}Mbps lower than the promised {self.promised_download}Mbps."
        elif self.dif_upload > self.marginal_error:
            tweet += f"My upload speed is {self.dif_upload}Mbps lower than the promised {self.promised_upload}Mbps."

        return tweet

