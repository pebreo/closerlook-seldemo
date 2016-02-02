#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.xvfb = os.environ.get("ENABLE_XVFB", False)
        self.browser = os.environ.get("BROWSER", "Chrome")
        if self.xvfb:
            self.vdisplay = Xvfb(width=1280, height=720)
            self.vdisplay.start()
        if self.browser == "Firefox":
            self.driver = self.get_ff_driver()
        else:
            self.driver = self.get_chrome_driver()
        self.load = self.driver.get

    def tearDown(self):
        if self.driver:
            self.driver.quit()
        if self.xvfb and self.vdisplay:
            self.vdisplay.stop()

    def get_ff_driver(self):
        return webdriver.Firefox()

    def get_chrome_driver(self):
        opts = Options()
        if "TRAVIS" in os.environ:  # github.com/travis-ci/travis-ci/issues/938
            opts.add_argument("--no-sandbox")
        # Fix for https://code.google.com/p/chromedriver/issues/detail?id=799
        opts.add_experimental_option("excludeSwitches",
                                     ["ignore-certificate-errors"])
        return webdriver.Chrome(chrome_options=opts)

    # def test_should_load_wikipedia(self):
    #     self.load("https://www.wikipedia.org")
    #     self.assertIn("Wikipedia", self.driver.title)

class TestCloserlook(BaseTestCase):
    
    #@unittest.skip('wip')
    def test_searchterm_not_found(self):
        """ Expect no search results when given a nonsense search term """
        self.driver.get('http://closerlook.com')
        self.driver.find_element_by_id('menu-search').click()
        self.driver.find_element_by_id('username').send_keys('thissearchtermwillnotbefound')
        self.driver.save_screenshot('noresultsfound_result.png')
        assert 'No results were found.' in self.driver.page_source


    def test_blank_searchterm(self):
        """ Expect redirect to mainpaige when given a blank search term """
        self.driver.get('http://closerlook.com')
        self.driver.find_element_by_id('menu-search').click()
        self.driver.find_element_by_id('username').send_keys('')
        self.driver.save_screenshot('redirect_result.png')
        assert 'Required' in self.driver.page_source


    def test_that_homepage_links_work(self):
        """
        All the homepage links should work.
        For more comprehensive test goto: http://validator.w3.org/checklink
        """
        self.driver.get('http://www.closerlook.com')
        links = self.driver.find_elements_by_xpath('//body//a[string-length(@href)>1]')
        
        # Filter only valid links
        links = [l for l in links if l.get_attribute('href').startswith('http://www.closerlook')]
        
        for link in links:
            href = link.get_attribute('href')
            print "Checking link %s" % href 
            # Use requests to grab headers of the links
            r = requests.get(href)
            assert r.headers
            assert r.status_code == 200

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
