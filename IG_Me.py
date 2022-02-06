#!/usr/bin/env python3
"""Create Instagram Bot."""
# -*- coding: UTF-8 -*-
from typing import List
import pandas as pd
import random
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import schedule


class IG_Bot:
    """Creating a Bot that acts like me."""

    def __init__(self, username, password):
        """Initialize Class."""
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]

        # Randomized User ID
        user_agent_rotator = UserAgent(software_name=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        chrome_options = Options()
        # chrome_option.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"user-agent={user_agent}")
        path = r'C:\Windows\chromedriver.exe'
        cookies_file_path = 'cookies.json'
        cookie_websites = ['https://Instagram.com']
        self.cookies_file_path = cookies_file_path
        self.cookie_websites = cookie_websites
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=path)
        try:
            # Load in cookies for the website
            cookies = json.load(open(self.cookies_file_path, "rb"))
            for website in self.cookie_websites:
                self.driver.get(website)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
        except Exception as e:
            print(str(e))
            print("Error Loading in Cookies")

    def save_cookie(self):
        """Save cookie."""
        json.dump(self.driver.get_cookies(), open("cookies.json", 'w'))

    # def load_cookie(self):
    #     """Load cookies into browser."""
    #     cookies = json.load(open('cookies.json', 'rb'))
    #     for cookie in cookies:
    #         self.driver.add_cookie(cookie)

    def login(self):
        """Login to Instagram."""
        if 'Instagram' in self.driver.title:
            print('Already logged in.')
            sleep(1.2)
            s_not_now = '/html/body/div[4]/div/div/div/div[3]/button[2]'
            self.driver.find_element_by_xpath(s_not_now).click()
        else:
            self.username = username
            self.password = password
            username_path = '//*[@id="loginForm"]/div/div[1]/div/label/input'
            password_path = '//*[@id="loginForm"]/div/div[2]/div/label/input'
            sleep(1)
            self.driver.find_element_by_xpath(
                username_path).send_keys(username)
            sleep(0.5)
            self.driver.find_element_by_xpath(
                password_path).send_keys(password)
            sleep(0.7)
            login_button = '//*[@id="loginForm"]/div/div[3]'
            self.driver.find_element_by_xpath(login_button).click()
            sleep(0.3)
            not_now = '//*[@id="react-root"]/section'\
                '/main/div/div/div/div/button'
            sleep(1.5)
            self.driver.find_element_by_xpath(not_now).click()
            sleep(1.5)
            s_not_now = '/html/body/div[4]/div/div/div/div[3]/button[2]'
            self.driver.find_element_by_xpath(s_not_now).click()

    def follow(self) -> str:
        """Follow fuction for evalute post."""
        follow_path = '/html/body/div[4]/div[2]/div/article/header/'\
            'div[2]/div[1]/div[2]/button'
        follow_ele = self.driver.find_element_by_xpath(follow_path)
        # if follow_ele.text == 'Follow':
        #     follow_ele.click()
        # Getting the Profile Username to return as string
        user_path = '/html/body/div[4]/div[2]/div/article/header/div[2]/'\
                    'div[1]/div[1]/span/a'
        return self.driver.find_element_by_xpath(user_path).text

    def evaluatePosts(self, tags, number_posts, just_like) -> List[str]:
        """Get tags to evaluate posts."""
        users_followed = []
        for tag in tags:
            t = 'https://Instagram.com/' + tag
            self.driver.get(t)
            sleep(1.5)
            self.driver.find_element_by_class_name('_9AhH0').click()
            like_button = '/html/body/div[4]/div[2]/div/'\
                + 'article/div[3]/section[1]/span[1]/button'
            for j in range(number_posts):
                video_watch_time = random.uniform(5, 10)
                photo_watch_time = random.uniform(4, 8)
                sleep(1.6)
                try:
                    # Video
                    v_a = '/html/body/div[4]/div[2]/div'\
                        + '/article/div[2]/div/div/div[3]'
                    v_p = self.driver.find_element_by_xpath(v_a)
                    v_p.click()
                    print('Watching Video for ', photo_watch_time, 'at index', j)
                    sleep(video_watch_time)
                    # liking the photo.
                    self.driver.find_element_by_xpath(like_button).click()
                    sleep(1)
                    # Follow person
                    # if not just_like:
                    #     users_followed += self.follow()
                    sleep(1.3)
                    self.driver.find_element_by_class_name(
                        'coreSpriteRightPaginationArrow').click()
                    sleep(1.5)
                except(NoSuchElementException, ElementClickInterceptedException):
                    # photo
                    print('Watching Photo for ', photo_watch_time, 'at index', j)
                    sleep(photo_watch_time)
                    self.driver.find_element_by_xpath(like_button).click()
                    sleep(1)
                    # if not just_like:
                    #     self.follow()
                    sleep(1.1)
                    self.driver.find_element_by_class_name(
                        'coreSpriteRightPaginationArrow').click()
                    sleep(1.25)
        return users_followed

    def Follow_Home(self, people) -> List[str]:
        """Follows people in the suggestive."""
        self.driver.get('https://www.instagram.com/explore/people/suggested/')
        sleep(1.2)
        self.driver.execute_script("window.scrollTo(0,100)")
        scroll_position = 100
        for i in range(1, people):
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/'
                    'div/div[2]/div/div/div[{}]/div[3]/'
                    'button'.format(i)).click()
                sleep(random.uniform(.3, .7))
            except (ElementClickInterceptedException):
                continue
            if i % 10 == 0:
                self.driver.execute_script("window.scrollTo({},{})".format(scroll_position,
                                                                           scroll_position + 625))
                scroll_position += 625

    def unfollow_people(self, webdriver, people_i_follow, people_to_unfollow):
        """people_i_follow will be a list of everyone I follow.
           people_to_unfollow will be a list of people that I will unfollow.
        """
        # if only one user, append in a list
        if (len(set(people_i_follow).intersection(set(people_to_unfollow))) > 1):
            for user in people_to_unfollow:
                try:
                    webdriver.get('https://www.instagram.com/' + user + '/')
                    sleep(5)
                    unfollow_xpath = '//*[@id="react-root"]/section/main/div/'\
                        'header/section/div[1]/div[1]/span/span[1]/button'

                    unfollow_confirm_xpath = '/html/body/div[3]/div/'\
                        'div/div[3]/button[1]'

                    if self.driver.find_element_by_xpath(unfollow_xpath).text == "Following":
                        sleep(random.randint(4, 15))
                        self.driver.find_element_by_xpath(unfollow_xpath).click()
                        sleep(2)
                        self.driver.find_element_by_xpath(unfollow_confirm_xpath).click()
                        sleep(4)
                        people_i_follow.remove(user)
                    # DBUsers.delete_user(user)
                except Exception:
                    traceback.print_exc()
                    continue
                return people_i_follow

    def unfollow(self, number, username):
        """Unfollows people from home."""
        self.driver.get('https://www.instagram.com/{}/'.format(username))
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section'
                '/main/div/header/section/ul/li[3]/a').click()
        except (ElementClickInterceptedException, NoSuchElementException):
            pass
        sleep(1.3)
        # Start the unfollowing process.
        unfollow_buttons = self.driver.find_elements_by_css_selector(
            '.sqdOP.L3NKy._8A5w5')
        count = 0
        for button in unfollow_buttons:
            if button.text == "Following":
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                '.sqdOP.L3NKy._8A5w5')))
                self.custom_wait_clickable_and_click()
                # actions = webdriver.ActionChains(self.driver)
                # actions.move_to_element(button).click().perform()
                # ele = WebDriverWait(self.driver, 20).until(
                #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[3]/button[1]')))
                # self.driver.find_element_by_xpath(
                #     '/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                # ele.click()
                # UNFOLLOW CONFIRMATION
                sleep(random.uniform(2, 4))
                count += 1
                if count > number:
                    break
        # for i in range(1, number):
        #     try:
        #         sleep(random.uniform(1, 2))
        #         self.driver.find_element_by_xpath(
        #             'html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button'.format(i)).click()
        #         sleep(random.uniform(1, 3))
        #         self.driver.find_element_by_xpath(
        #             '/html/body/div[5]/div/div/div/div[3]/button[1]').click()
        #         sleep(random.uniform(1, 5))
        #     except (ElementClickInterceptedException):
        #         continue
        # pass

        # if __name__ == '__main__':
        # data = pd.read_csv('Secret.txt', header=None)
        # username = data.iloc[0][0]
        # password = data.iloc[1][0]
        # bot = IG_Bot(username, password)
        # bot.login()
        # tags = pd.read_csv('tags.txt', header=None)
        # tags = tags.iloc[:, 0]
        # sleep(1.3)
        # bot.Follow_Home(random.randint(5, 15))
        # bot.evaluatePosts(tags, random.randint(2, 4), True)
        # bot.save_cookie()


def main_runner():
    """Use for running script with a cron job."""
    data = pd.read_csv('Secret.txt', header=None)
    tags = pd.read_csv('tags.txt', header=None)
    tags = tags.iloc[:, 0]
    username = data.iloc[0][0]
    password = data.iloc[1][0]
    # Bot functionality...
    bot = IG_Bot(username, password)
    bot.login()
    sleep(1.3)
    # # Apparently requests to follow are 20 an hour
    # bot.Follow_Home(random.randint(15, 20))
    # sleep(1.6)
    users_followed = bot.evaluatePosts(random.choices(tags, k=1),
                                       random.randint(1, 1), True)
    with open('users_followed.txt', "a+") as file:
        file.write(json.dumps(users_followed))

    # sleep(.5)
    # Saving cookies..

    # Unfollowing process (done only after I am done liking/following others)
    # bot.unfollow(random.randint(5, 7), username)
    # sleep(random.uniform(3, 7))
    # print("Finished running script.")
    # bot.save_cookie()
    # print('Closing Process...')
    # bot.driver.quit()


if __name__ == '__main__':
    # schedule.every().hour.do(main_runner)

    data = pd.read_csv('Secret.txt', header=None)
    tags = pd.read_csv('tags.txt', header=None)
    tags = tags.iloc[:, 0]
    username = data.iloc[0][0]
    password = data.iloc[1][0]
    # Bot functionality...
    bot = IG_Bot(username, password)
    bot.login()
    # sleep(1.3)
    # users_followed = bot.evaluatePosts(random.choices(tags, k=3),
    #                                    random.randint(2, 3), False)
    # sleep(1.8)
    # with open('users_followed.txt', "a+") as file:
    #     file.write(json.dumps(users_followed))
    # main_runner()
    # schedule.every(45).minutes.do(main_runner)
    # while True:
    #     schedule.run_pending()
    #     sleep(1)
