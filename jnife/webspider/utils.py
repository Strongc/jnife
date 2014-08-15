# -*- coding: utf-8; -*-

import os
from ConfigParser import ConfigParser
import urllib
from selenium import webdriver
from selenium.webdriver.common.proxy import *

class User(object):
    """
    Utility class for webspider, used to get username & password from a local config file. 
    
    The config file is a "standard ini file":http://en.wikipedia.org/wiki/INI_file.
    By default, we assume the config file is "~/.webuser.ini".
    A sample of this file as below: 
    
        [google]
        user = <your-user-name>
        password = <your-password>
    
    """
    
    def __init__(self, ):
        """
        """
        self.config_file = os.path.join(os.path.expanduser("~"), ".webuser.ini")
        self.conf = ConfigParser()
        self.conf.read(self.config_file)

    def get_user_pwd(self, site):
        """
        Get username & password
        
        Arguments:
        - `self`:
        - `site`: site name. e.g.: google
        
        Return a tuple. (username, password)
        """
        user = self.conf.get(site, "user")
        pwd = self.conf.get(site, "password")
        return (user, pwd)


def parse_verify_code(src):
    """parse image verify code
    
    Arguments:
    - src: image src
    """
    urllib.urlretrieve(imgsrc, 'codeimg.jpg')
    # parse

    
def get_firefox_profile(profile_dir=None):
    """
    return webdriver.FirefoxProfile

    Arguments:
    - `profile_dir`: if not set, default value is "~/.mozilla/firefox/selenium"
    """
    user_home = os.path.expanduser("~")
    if not profile_dir:
        profile_dir = os.path.join(user_home, '.mozilla/firefox/selenium')
    profile = webdriver.FirefoxProfile(profile_dir)

    # prevent download dialog
    download_dir = os.path.join(user_home, 'Downloads', 'selenium')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream");
    return profile


def get_firefox(use_profile=False, proxy=None, profile_dir=None):
    """
    
    Arguments:
    - `use_profile`: 
    - `proxy`:
    - `profile_dr`: 
    """
    profile = None
    _proxy = None
    if use_profile:
        profile = get_firefox_profile(profile_dir)
    if proxy:
        _proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'ftpProxy': proxy, 
            'sslProxy': proxy,
            'noProxy': ''
        })
        
    driver = webdriver.Firefox(firefox_profile=profile, proxy=_proxy)
    return driver

    
