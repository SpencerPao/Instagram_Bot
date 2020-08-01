#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This is an Instagram Runner script.

Needs a Secrets file (Username and password)
Needs a hashkey file (search values)
"""

from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import pandas as pd
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.webdriver.common.proxy import Proxy, ProxyType


class IG_Bot_Creation:
    """Class creation for the bot itself."""

    def __init__(self, username, password, ProxyList) -> None:
        """Initialize the bot."""
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        # Getting a random user agent
        # Changing up the user identifier.
        user_agent = user_agent_rotator.get_random_user_agent()
        chrome_options = Options()
        # Won't physically open a browser on my machine.
        # chrome_options.add_argument("--headless")
        # Only way to get chromedriver to open headlessly (ignore firefox)
        chrome_options.add_argument("--no-sandbox")
        # Apparently needed for window machines
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"user-agent={user_agent}")
        path = r'C:\Windows\chromedriver.exe'
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=path)
        self.driver.get('https://Instagram.com')
        self.driver.maximize_window()

    def login(self) -> None:
        """Login to Instagram using the secrets file."""
        sleep(2)
        # username setting
        self.username = username
        username_path = '//*[@id="react-root"]/section/main/article/',\
            'div[2]/div[1]/div/form/div[2]/div/label/input'
        # self.driver.find_element_by_xpath(username_path).send_keys(username)
        self.driver.find_element_by_xpath(
            username_path[0] + username_path[1]).send_keys(username)

        sleep(2)
        # Password setting
        self.password = password
        password_path = '//*[@id="react-root"]/section/main/article/',\
            'div[2]/div[1]/div/form/div[3]/div/label/input'
        self.driver.find_element_by_xpath(
            password_path[0]+password_path[1]).send_keys(password)
        login_path = '//*[@id="react-root"]/section/main/article/',\
            'div[2]/div[1]/div/form/div[4]/button'
        self.driver.find_element_by_xpath(login_path[0]+login_path[1]).click()
        sleep(2)
        # Get out of the notifcations
        self.driver.find_elements_by_xpath(
            "//button[contains(text(), 'Not Now')]")[0].click()
        sleep(1)
        # Other notifcations (second screne that popped up)
        self.driver.find_element_by_xpath(
            "//*[contains(@class, 'aOOlW   HoLwm ')]").click()

    def FollowOrNot(self, score) -> None:
        """Determine whether or not to follow the person (HELPER FUNCTION)."""
        if score > 0.3:
            # If I am already following this person, cancel out.
            try:
                print('Attempting to follow this person')
                sleep(0.5)
                followPath = '/html/body/div[4]/div[2]/div/article/',\
                    'div/header/div[2]/div[1]/div[2]/button'
                fb = self.driver.find_element_by_xpath(followPath[0] +
                                                       followPath[1])
                fb.click()
                try:
                    if self.driver.find_element_by_xpath(
                            '//*[text()="Cancel"]'):
                        cancel_path = '//*[text()',\
                            '="Cancel"]'
                        self.driver.find_element_by_xpath(cancel_path[0] +
                                                          cancel_path[1]
                                                          ).click()
                except NoSuchElementException:
                    pass
            except NoSuchElementException:
                print('Couldnt find the follow button..')
                pass
        else:
            print('Not following this person')

    def likePost(self, scoreValue, followValue) -> None:
        """Evaluate whether to like post or not (HELPER FUNCTION)."""
        if (scoreValue > 20):
            try:
                print('Attempting to like photo')
                likeButton = '/html/body/div[4]/div[2]/div/article/',\
                    'div/div[3]/section[1]/span[1]/button'
                self.driver.find_element_by_xpath(likeButton[0]+likeButton[1]
                                                  ).click()
                sleep(0.5)
                self.FollowOrNot(followValue)
                self.driver.find_element_by_class_name(
                    'coreSpriteRightPaginationArrow').click()
                sleep(1.5)
            except NoSuchElementException:
                print('Cant find like button')
                self.driver.find_element_by_class_name(
                    'coreSpriteRightPaginationArrow').click()
        else:
            sleep(0.53)
            # The Next Picture button
            self.driver.find_element_by_class_name(
                'coreSpriteRightPaginationArrow').click()

    def evaluatePost(self, amount):
        """Goes through the posts (homepage) to like and follow at will."""
        # Opens the very first post in the hastag
        self.driver.find_element_by_class_name('_9AhH0').click()
        i = 1
        while i <= amount:
            likeValue = random.uniform(0, 100)
            print("Post #: ", i, 'Probability of Liking Photo', likeValue)
            # Looking at photo
            picture_time = random.uniform(2, 8)
            # Watching video
            video_time_watch = random.uniform(5, 15)
            # Probability of you falling the person if you like photo
            follow_value = random.uniform(0, 1)
            # probabilty of likeing Photo
            # If video do this
            sleep(1.5)
            try:
                # Checking to see if video
                # If it is not a video, it will throw an exceptions
                # if a video... watch it.
                v_path = '/html/body/div[4]/div[2]/div/article/',\
                    'div/div[2]/div/div/div[3]'
                video_play = self.driver.find_element_by_xpath(
                    v_path[0]+v_path[1])
                # Watch the video
                video_play.click()
                print("Video time watching : ", video_time_watch)
                sleep(video_time_watch)
                self.likePost(likeValue, follow_value)
            except (NoSuchElementException,
                    ElementClickInterceptedException):
                print("Picture time watching : ", picture_time)
                sleep(picture_time)
                self.likePost(likeValue, follow_value)

            i = i+1

    # Hash is the search query to look into
    # -- I need to work on this further ---
    def Follow_Home_List_People(self, amount):
        """Home Screen follow a 'amount' of people."""
        for i in range(amount):
            try:
                self.driver.find_element_by_xpath("//*[text()',\
                '='Follow']").click()
                sleep(random.uniform(1, 2))
                """
                    If I see the unfollow button, click cancel
                """
                try:
                    if self.driver.find_element_by_xpath(
                            "//*[text()='Cancel']"):
                        cancel_path = "//*[text()',\
                        '='Cancel']"
                        self.driver.find_element_by_xpath(cancel_path[0] +
                                                          cancel_path[1]
                                                          ).click()
                except NoSuchElementException:
                    pass
            except NoSuchElementException:
                print('No button found')


# Getting the list of proxies (only 100 in list)
# ua = UserAgent() # From here we generate a random user agent


# --------------------------------------
# PUBLIC PROXIES ARE USED TOO MUCH
# I MIGHT HAVE TO PAY FOR SERVICES TO CONTINUE WITH THE
# PROXY idea
# Refer to the proxy.py file for configuration details if I go this route
# --------------------------------------
proxies = []  # Will contain proxies [ip, port]
# proxies_req = Request('https://www.sslproxies.org/')
# proxies_req.add_header('User-Agent', ua.random)
# proxies_doc = urlopen(proxies_req).read().decode('utf8')
# soup = BeautifulSoup(proxies_doc, 'html.parser')
# proxies_table = soup.find(id='proxylisttable')
# # Save proxies in the array
# for row in proxies_table.tbody.find_all('tr'):
#   proxies.append({
#     'ip':   row.find_all('td')[0].string,
#     'port': row.find_all('td')[1].string
#   })
# Reading password file
if __name__ == "__main__":
    d = pd.read_csv('Secret.txt', header=None)
    username = d.iloc[0][0]
    password = d.iloc[1][0]
    # Passing in Username and Password and List of proxies to potentially use
    bot = IG_Bot_Creation(username, password, proxies)
    bot.login()
    sleep(2)
    # bot.Follow_Home_List_People(5)
    bot.driver.get('https://Instagram.com/explore/tags/mountain/')
    bot.evaluatePost(5)
# ss
