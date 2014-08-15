#!/usr/bin/python

import os
from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import logging
import datetime
from jnife import logconf


PROXY_FILE = os.path.join(os.path.dirname(__file__), 'validate.txt') # 'proxy.txt'

logger = logging.getLogger(__name__)


def check():
    """
    """
    proxies = get_all_proxies(PROXY_FILE)
    ret = validate_proxies(proxies) 
    logger.info('%d proxies, %d is available, %d is unavailable.' % (
        len(proxies), len(ret[0]), len(ret[1])))
    logger.debug('\n available proxies')
    logger.debug('------------------------')
    logger.debug('\n'.join(ret[0]))


def get_all_proxies(file=None):
    """
    Return all proxies

    Arguments:
    - `file`: proxy file
    """
    if not file:
        file = PROXY_FILE
    return [line.strip() for line in open(file)]
    
        
def validate_proxies(proxies, test_url=None):
    """
    Return tuple. 
    First element is available proxies list. 
    Second element is unavailable proxies list

    Arguments:
    - `proxies`:
    """
    availabes, unavailables = [], []
    # for proxy in proxies:
    #     if is_proxy_available(proxy, test_url):
    #         availabes.append(proxy)
    #     else:
    #         unavailables.append(proxy)
    # return (availabes, unavailables)

    def worker(proxy):
        if is_proxy_available(proxy, test_url):
            availabes.append(proxy)
        else:
            unavailables.append(proxy)
    
    pool = ThreadPool(10)
    pool.map(worker, proxies)
    pool.close()
    pool.join()
    return (availabes, unavailables)
    
    
def is_proxy_available(proxy, test_url=None):
    """
    Return Bool. True if the proxy availabe.

    Arguments:
    - `proxy`: String. eg: "10.10.10.10:80"
    """
    if not test_url:
        test_url= 'http://www.baidu.com/'
    # proxy_cfg = {'http': 'http://'+proxy }

    logger.debug('Validating %s ...' % proxy)
    
    time_start = datetime.datetime.now()
    # status_code = urllib.urlopen(TEST_URL, proxies=proxy_cfg).getcode()

    opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy}))
    urllib2.install_opener(opener)
    try:
        status_code = urllib2.urlopen(test_url, timeout=2).getcode()
    except Exception, e:
        # logger.exception("error occure!")
        return False
    
    time_elapse = datetime.datetime.now() - time_start
    
    logger.debug('Status code is %d . Cost %s s.' % (status_code, time_elapse))
    return status_code == 200
    


if __name__ == '__main__':
    check()


