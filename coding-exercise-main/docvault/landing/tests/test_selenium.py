from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest


@unittest.skip("This test requires Chrome Web Driver")
class LandingTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("C:/Windows/chromedriver.exe")

    def test_search_in_python_org(self):
        driver = self.driver

        driver.get("http://docvault37.eba-8bqt95tj.us-west-2.elasticbeanstalk.com/")
        self.assertEquals("DocVault", driver.title)

    def tearDown(self):
        self.driver.close()
