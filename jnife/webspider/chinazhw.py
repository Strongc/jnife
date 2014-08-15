#!/usr/bin/python
# -*- coding: utf-8; -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, re, random, argparse
from utils import User

class ChinaZHW(object):
    """
    """
    
    def __init__(self, webDesc):
        """
        """
        self.webDesc = webDesc
        self.driver = webdriver.Firefox()
        self.base_url = self.webDesc.get_base_url()
        self.forum_max_limit = 7
        self.thread_max_limit = 6
        self.visit_max_limit = 100
        self.time_gap_per_reply = 10
        self.reply_counter = 0

    def close(self):
        """
        """
        self.driver.quit()

    def login(self):
        """
        Login chinazhw
        Arguments:
        - `self`:
        """
        self.webDesc.login(self.driver)
        
    def bump(self):
        """
        
        Arguments:
        - `self`:
        """
        try:
            self.webDesc.login(self.driver)
            time.sleep(10)
            self.traval_rand_post()
            
        except Exception, ex:
            print "Oops! Some errors occur!"
            print ex
        finally:
            self.close()
        

    def reply_post(self, url, text):
        """
        
        Arguments:
        - `self`:
        """
        driver = self.driver
        # driver.get(url)
        driver.find_element_by_id("fastpostmessage").clear()
        driver.find_element_by_id("fastpostmessage").send_keys(text)
        driver.find_element_by_id("fastpostsubmit").click()
        print "reply post. url: %s ; text: %s" % (url, text)


    def traval_rand_post(self):
        driver = self.driver
        driver.get(self.base_url);
        forums = driver.find_elements_by_css_selector("a[href^='forum']")
        forums_len = len(forums)
        if(forums_len == 0):
            return
        forums_counter = min(self.forum_max_limit, forums_len)
        forums_url = map(lambda el: el.get_attribute('href'), random.sample(forums, forums_counter))

        for forum_url in forums_url:
            print "visiting %s" % forum_url
            driver.get(forum_url)
            threads = driver.find_elements_by_css_selector("a[href^='thread']")
            threads_len = len(threads)
            if(threads_len == 0):
                continue
                
            threads_counter = min(self.thread_max_limit, threads_len)
            threads_url = map(lambda el: el.get_attribute('href'), random.sample(threads, threads_counter))
            for thread_url in threads_url:
                print "visiting thread url %s" % thread_url
                driver.get(thread_url)
                # get text
                replys = driver.find_elements_by_css_selector(".t_f")
                replys_len = len(replys)
                reply_text = ""
                if(replys_len < 2):
                    reply_text = u"抢沙发, 哈哈, 楼主好人, 小手抖抖, 金币到手...."
                else:
                    reply_text = replys[replys_len-1].get_attribute('textContent')
                    
                try:
                    self.reply_post(thread_url, reply_text)
                    self.reply_counter+=1
                    if(self.time_gap_per_reply > 0):
                        time.sleep(self.time_gap_per_reply)
                except Exception, ex:
                    print "post reply errors!"
                    print ex
                
        print "Reply totally %d" % self.reply_counter

        
class WebDesc(object):
    """
    Interface: Web description.
    """
    
    def get_website_name(self):
        """
        
        Arguments:
        - `self`:
        """
        raise "Need to be implemented"

    def get_base_url(self):
        """
        
        Arguments:
        - `self`:
        """
        raise "Need to be implemented"        
        
    def login(self, driver):
        """
        
        Arguments:
        - `self`:
        - `driver`:
        """
        raise "Need to be implemented"

        
class ChinaZhwDesc(WebDesc):
    
    def get_website_name(self):
        """
        
        Arguments:
        - `self`:
        """
        return "真好论坛"

    def get_base_url(self):
        """
        
        Arguments:
        - `self`:
        """
        return "http://www.chinazhw.com"
        
    def login(self, driver):
        """
        
        Arguments:
        - `self`:
        - `driver`:
        """
        upw = User().get_user_pwd('chinazhw')
        print "user %s login chinazhw ." % upw[0]
        driver.get(self.get_base_url() + "/forum.php")
        driver.find_element_by_id("ls_username").clear()
        driver.find_element_by_id("ls_username").send_keys(upw[0])
        driver.find_element_by_id("ls_password").clear()
        driver.find_element_by_id("ls_password").send_keys(upw[1])
        driver.find_element_by_xpath("//button[@type='submit']").click()
        

def main():
    """
    """
    zhw = ChinaZHW(ChinaZhwDesc())

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # login command
    login_parser = subparsers.add_parser('login', help='Login Chinazhw')
    login_parser.set_defaults(func=lambda args: zhw.login())

    # bump command
    bump_parser = subparsers.add_parser('bump', help='to bump :)')
    bump_parser.set_defaults(func=lambda args: zhw.bump())

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception, e:
        print e
    finally:
        zhw.close()
    
if __name__ == "__main__":
    main()

