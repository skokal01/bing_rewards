import unittest
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import requests
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class FixturesTest(unittest.TestCase):

   def setUp(self):
        self.driver = None
        self.base_url = "http://www.bing.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.story_titles = []
        self.max_users = 3
        self.max_searches = 36

   def fetch_top_stories(self):
        requests.packages.urllib3.disable_warnings()
        hckr_news_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        hckr_stry_url = "https://hacker-news.firebaseio.com/v0/item/%s.json"

        # Get base hacker news stories
        r = requests.get(hckr_news_url, verify=False)
        stories = r.json()

        # Get each story title
        index = 0
        for story in stories:
           r = requests.get(hckr_stry_url % (story), verify=False)
           self.story_titles.append(r.json()['title'])
           index = index + 1
           print index, r.json()['title']
           if index == self.max_users * self.max_searches:
              break

   def login_bing(self, user_name, password):
        driver = self.driver
        driver.get(self.base_url + "/")

        # Login
        driver.find_element_by_id("id_s").click()
        driver.find_element_by_css_selector("span.id_name").click()
        driver.find_element_by_id("i0116").clear()
        driver.find_element_by_id("i0116").send_keys(user_name)
        driver.find_element_by_id("i0118").clear()
        driver.find_element_by_id("i0118").send_keys(password)
        driver.find_element_by_id("idChkBx_PWD_KMSI0Pwd").click()
        driver.find_element_by_id("idSIButton9").click()

   def logout_bing(self):
        # Logout
        driver = self.driver
        driver.find_element_by_id("id_l").click()
        driver.find_element_by_css_selector("span.id_name").click()
        driver.find_element_by_id("id_l").click()
        driver.find_element_by_css_selector("span.id_name").click()              

   def query_bing(self):
        driver = self.driver
        for x in range(0, self.max_searches):
           queryStr = self.story_titles.pop()
           driver.find_element_by_id("sb_form_q").clear()
           driver.find_element_by_id("sb_form_q").send_keys(queryStr)
           driver.find_element_by_id("sb_form_go").click()
           driver.find_element_by_id("sb_form_q").click()
                   
   def get_rewards(self, user_name, password):
        self.login_bing(user_name, password)
        self.query_bing()
        time.sleep(3)
        self.logout_bing()

   def test_bing(self):
        # get top story titles from hackernews
        self.fetch_top_stories()

        # Launch firefox web-browser
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
                
        self.get_rewards("<USER1>", "<USER1 PASSWORD>")
        self.get_rewards("<USER2>", "<USER2 PASSWORD>")
        self.get_rewards("<USER3>", "<USER3 PASSWORD>")

   def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()
