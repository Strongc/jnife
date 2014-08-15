#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import TimeoutException
import argparse

def open_firefox_with_proxy(proxy_str):
    """
    """
    
    # proxy_str = "182.118.23.7:8081"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy_str,
        'ftpProxy': proxy_str, 
        'sslProxy': proxy_str,
        'noProxy': ''
    })

    driver = webdriver.Firefox(proxy=proxy)
    return driver
    

def open_firefox():
    driver = webdriver.Firefox()
    return driver


def show_ips(driver):
    """
    """
    driver.get('http://www.ip.cn/') 
    ip = driver.find_element_by_css_selector("#result code").text
    loc = driver.find_elements_by_css_selector("#result p")[1].text
    print "ip: %s" % ip
    print "location: %s" % loc


def main():
    parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(help='commands')
    parser.add_argument('-p', action='store', metavar='PROXY',
                        dest='proxy', default=None, 
                        help='proxy to be used')
    
    args = parser.parse_args()
    if args.proxy:
        driver = open_firefox_with_proxy(args.proxy)
        print 'with proxy'
    else:
        driver = open_firefox()
        print 'without proxy'
    try:
        show_ips(driver)
    except Exception as e:
        print e
        driver.close()
        
    
if __name__ == '__main__':
    main()
