#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, os
from selenium import webdriver
from selenium.webdriver.common.proxy import *

DEFAULT_PROFILE = os.path.join(os.path.expanduser('~'), '.mozilla/firefox', '2zzkxax3.default-1405513858554')

def get_default_profile_dir():
    p_dir = os.path.join(os.path.expanduser('~'), '.mozilla/firefox')
    dirs = os.listdir(p_dir)
    default_dir = filter(lambda d: 'default' in d, dirs)[0]
    return os.path.join(p_dir, default_dir)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxy', action='store', metavar='PROXY',
                        dest='proxy', default=None, help='proxy to be used')
    parser.add_argument('-d', '--default-profile', action='store_true', default=False,
                        dest='default_profile', help='start firefox with default profile')
    parser.add_argument('--profile-dir', action='store', dest='profile_dir',
                        help='specify the profile to used. if profile enable. '\
                        'By default, it will use default profile')

    args = parser.parse_args()

    if args.default_profile or args.profile_dir:
        profile_dir = args.profile_dir or get_default_profile_dir()
        profile = webdriver.FirefoxProfile(profile_dir)
    else:
        profile = None

    proxy = None
    if args.proxy:
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': args.proxy,
            'ftpProxy': args.proxy, 
            'sslProxy': args.proxy,
            'noProxy': ''
        })

    driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)
    

if __name__ == '__main__':
    main()
    
