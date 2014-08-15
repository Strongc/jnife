#!/usr/bin/python
# -*- coding: utf-8; -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, re, random, argparse, logging
from contextlib import closing
from utils import User, get_firefox_profile
from jnife import logconf

logger = logging.getLogger(__name__)

class YiYiPan(object):
    """
    """
    
    def __init__(self, driver=None):
        """
        """
        upw = User().get_user_pwd('yiyipan')
        self.driver = driver if driver else webdriver.Firefox(get_firefox_profile())
        self.base_url = "http://www.yiyipan.com"
        self.user = upw[0]
        self.password = upw[1]

    def close(self):
        """
        """
        self.driver.quit()

    def download(self, url):
        driver = self.driver
        driver.get(url)
        driver.find_element_by_id("hsdownload").click()

        # close current window & move to the new open window
        driver.close()
        driver.switch_to_window(driver.window_handles[-1])
        # show download buttons
        driver.execute_script('document.getElementById("down_box").style.display="block"')
        # driver.find_element_by_css_selector("#down_box a[title='高速一']").click()
        driver.find_element_by_link_text(u"高速一").click()
        logger.info('download from %s' % url)
        return self
        

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    download_parser = subparsers.add_parser('download', help='download file from yiyipan')
    download_parser.add_argument('url', action='store', metavar='URL',
                                 help='the url which will be download')
    download_parser.set_defaults(func=lambda args: YiYiPan().download(args.url))

    args = parser.parse_args()
    with closing(args.func(args)):
        time.sleep(20)
        logger.info('close firefox')


if __name__ == '__main__':
    main()
    
