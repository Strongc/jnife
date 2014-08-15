#!/usr/bin/python
# -*- coding: utf-8; -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, re, random, argparse, logging
from contextlib import closing
from utils import User
from jnife import logconf

logger = logging.getLogger(__name__)


class YunFile(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        upw = User().get_user_pwd('yunfile')
        self.driver = webdriver.Firefox()
        self.base_url = "http://www.yunfile.com"
        self.user = upw[0]
        self.password = upw[1]

    def close(self):
        """
        """
        self.driver.quit()
        
    def login(self):
        """
        Login to yunfile

        Arguments:
        - `self`:
        """
        logger.info('use %s to login yunfile' % self.user)
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_userid").clear()
        driver.find_element_by_id("login_userid").send_keys(self.user)
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys(self.password)
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        return self

    def upload(self, file):
        """
        Upload file to yunfile

        Arguments:
        - `self`:
        - `file`: file name
        """
        self.login()
        time.sleep(10)
        logger.info( 'upload file: %s' % file )
        driver = self.driver
        driver.get(self.base_url + "/user/forPartners.html")
        driver.find_element_by_link_text(u"上传接口").click()
        driver.find_element_by_link_text(u"普通上传").click()
        # driver.find_element_by_id("file").clear()
        driver.find_element_by_id("file").send_keys(file)
        driver.find_element_by_id("uploadButton").click()
        return self


        
def main():

    # def login(args):
    #     with closing(YunFile().login()):
    #         print "login..."

    # def upload(args):
    #     with closing(YunFile().login(args.file)):
    #         print "upload..."
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # login command
    login_parser = subparsers.add_parser('login', help='Login yunfile')
    login_parser.set_defaults(func=lambda args: YunFile().login())

    # upload command
    upload_parser = subparsers.add_parser('upload', help='Upload file to yunfile')
    upload_parser.add_argument('file', action='store', metavar='FILE',
                               help='upload file to yunfile')
    upload_parser.set_defaults(func=lambda args: YunFile().upload(args.file))

    # parse args & call relative functions
    args = parser.parse_args()
    
    with closing(args.func(args)):
        logger.info("close firefox")

    
if __name__ == '__main__':
    main()
