#!/usr/bin/python
# -*- coding: utf-8; -*-

import logging, time, random, os
import urllib2, socket, httplib
from multiprocessing.dummy import Pool as ThreadPool 
from jnife import logconf
from jnife.proxy import proxy as p
from jnife.webspider.yiyipan import YiYiPan
from jnife.webspider.utils import get_firefox

logger = logging.getLogger(__name__)


def get_downurls():
    """
    """
    # jcshaka
    # urls = ["file-2688.html", "file-2687.html", "file-2686.html", "file-2685.html", "file-2684.html", "file-2683.html", "file-2682.html", "file-2681.html", "file-2680.html", "file-2679.html", "file-2678.html", "file-2677.html", "file-2676.html", "file-2675.html", "file-2674.html", "file-2673.html", "file-2672.html", "file-2671.html", "file-2670.html", "file-2669.html"]
    # urls += ["file-2648.html", "file-2647.html", "file-2646.html", "file-2645.html", "file-2644.html", "file-2643.html", "file-2642.html", "file-2641.html", "file-2640.html", "file-2639.html", "file-2638.html", "file-2637.html", "file-2636.html", "file-2635.html", "file-2634.html", "file-2633.html", "file-2632.html", "file-2631.html", "file-2630.html", "file-2629.html"]
    # urls += ["file-2628.html", "file-2627.html", "file-2626.html", "file-2625.html", "file-2624.html", "file-2623.html", "file-2622.html", "file-2621.html", "file-2620.html", "file-2619.html", "file-2618.html", "file-2617.html", "file-2616.html", "file-2615.html", "file-2614.html", "file-2613.html", "file-2612.html", "file-2611.html", "file-2610.html", "file-2609.html"]
    # urls += ["file-2534.html", "file-2533.html", "file-2532.html", "file-2531.html", "file-2530.html", "file-2529.html", "file-2528.html", "file-2527.html", "file-2526.html", "file-2524.html"]

    # # exceldream
    # urls += ["file-2668.html", "file-2667.html", "file-2666.html", "file-2665.html", "file-2664.html", "file-2663.html", "file-2662.html", "file-2661.html", "file-2660.html", "file-2659.html", "file-2658.html", "file-2657.html", "file-2656.html", "file-2655.html", "file-2654.html", "file-2653.html", "file-2652.html", "file-2651.html", "file-2650.html", "file-2649.html"]
    # urls += ["file-2608.html", "file-2607.html", "file-2606.html", "file-2605.html", "file-2604.html", "file-2603.html", "file-2602.html", "file-2601.html", "file-2600.html", "file-2599.html", "file-2598.html", "file-2597.html", "file-2596.html", "file-2595.html", "file-2594.html", "file-2593.html", "file-2592.html", "file-2591.html", "file-2590.html", "file-2589.html"]
    # urls += ["file-2391.html", ]
    
    # return map(lambda u: 'http://www.yiyipan.com/%s' % u, urls)
    return ['http://www.yiyipan.com/file-2688.html', 'http://www.yiyipan.com/file-2687.html']

def download(proxy):
    """
    Arguments:
    - `proxy`:
    """
    urls = get_downurls()
    random.shuffle( urls )
    is_available = p.is_proxy_available(proxy, urls[0])
    logger.info('%s is %s' % (proxy, 'available' if is_available else 'unavailable'))
    if is_available:
        pid = "" if not hasattr(os, 'getppid') else os.getppid()
        logger.info('%s use proxy %s ' % (pid, proxy))
        driver = get_firefox(True, proxy)
        driver.set_page_load_timeout(100)
        yiyipan = YiYiPan(driver)
        for url in urls:
            try:
                yiyipan.download(url)
                time.sleep(10)
            # except urllib2.URLError as e:
            #     print type(e)    
            except socket.timeout as e: # timeout
                logger.error('timeout exception. ...')
                logger.error( type(e) )
            except Exception as e:
                if isinstance(e, httplib.CannotSendRequest):
                    logger.error( 'Catch exception: CannotSendRequest')
                    logger.error(type(e))
                else:
                    logger.error(type(e))
        driver.close()

        
def _main():
    proxies = p.get_all_proxies()
    random.shuffle(proxies)
    pool = ThreadPool(2)
    pool.map(download, proxies[:100])
    pool.close()
    pool.join()
    

def main():
    proxies = p.get_all_proxies()
    random.shuffle(proxies)
    for proxy in proxies:
        download(proxy)

    
if __name__ == '__main__':
    main()
    
