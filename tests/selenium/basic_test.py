#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Test(unittest.TestCase):

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

    def test_should_load_wikipedia(self):
        self.load("https://www.wikipedia.org")
        self.assertIn("Wikipedia", self.driver.title)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
