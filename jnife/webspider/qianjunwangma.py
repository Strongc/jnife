#!/usr/bin/python
# -*- coding: utf-8; -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, re, random, argparse, logging, urllib
from contextlib import closing
from utils import User, parse_verify_code
from jnife import logconf

logger = logging.getLogger(__name__)


class QianJunWangMa(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        upw = User().get_user_pwd('7958')
        self.driver = webdriver.Firefox()
        self.base_url = "http://www.7958.com"
        self.user = upw[0]
        self.password = upw[1]

    def close(self):
        """
        """
        self.driver.quit()
        
    def login(self):
        """
        Login to 7958.com

        Arguments:
        - `self`:
        """
        logger.info('use %s to login 7958.com' % self.user)
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//img[contains(@src,'http://img1.7958.com/static/disk/images/head_ljdl.gif')]").click()
        time.sleep(5)
        driver.find_element_by_id("username_$loginhash").clear()
        driver.find_element_by_id("username_$loginhash").send_keys(self.user)
        driver.find_element_by_id("password3_$loginhash").clear()
        driver.find_element_by_id("password3_$loginhash").send_keys(self.password)
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()        
        return self

    def upload(self, file):
        """
        Upload file to 7958.com
        As the uploader use flash swf object. Selemium can not work with it.

        Arguments:
        - `self`:
        - `file`: file name
        """
        # self.login()
        # time.sleep(10)
        # logger.info( 'upload file: %s' % file )
        # driver = self.driver
        # driver.find_element_by_link_text(u"上传文件").click()
        # driver.find_element_by_id('SWFUpload_0').click()
        # driver.find_element_by_id('SWFUpload_0').send_keys(file)
        # driver.find_element_by_css_selector("input.start").click()
        # driver.find_element_by_id("do_share").click()
        # driver.find_element_by_css_selector("a.close").click()
        return self

    def download(self, url):
        """
        download file from 7958.com

        Arguments:
        - `self`:
        - `url`:
        """
        driver = self.driver
        driver.get(url)
        driver.find_element_by_xpath("//img[contains(@src,'http://img1.7958.com/static/v4/images/dianxin.gif')]").click()
        driver.find_element_by_id("valcode").clear()

        codeImg = driver.find_element_by_id('codeimg')
        imgsrc = codeImg.get_attribute('src')
        valcode = parse_verify_code(imgsrc)
        driver.find_element_by_id("valcode").send_keys(valcode)
        driver.find_element_by_id("btnCode").click()
        return self

        
def main():

    # def login(args):
    #     with closing(QianJunWangMa().login()):
    #         print "login..."

    # def upload(args):
    #     with closing(QianJunWangMa().login(args.file)):
    #         print "upload..."
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # login command
    login_parser = subparsers.add_parser('login', help='Login 7958.com')
    login_parser.set_defaults(func=lambda args: QianJunWangMa().login())

    # upload command
    upload_parser = subparsers.add_parser('upload', help='Upload file to 7958.com')
    upload_parser.add_argument('file', action='store', metavar='FILE',
                               help='upload file to 7958.com')
    upload_parser.set_defaults(func=lambda args: QianJunWangMa().upload(args.file))

    # parse args & call relative functions
    args = parser.parse_args()
    
    with closing(args.func(args)):
        logger.info("close firefox")

    
if __name__ == '__main__':
    main()
