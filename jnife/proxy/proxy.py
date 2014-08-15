
import validate as V

def get_all_proxies(file=None):
    """
    """
    return V.get_all_proxies(file)

def is_proxy_available(proxy, test_url=None):
    """
    Check if the proxy available

    Arguments:
    - `proxy`: string. e.g. 10.10.10.10:8888
    """
    return V.is_proxy_available(proxy, test_url)

def get_available_proxies(file=None, test_url=None):
    """
    Get urls which have been verified that available
    
    Arguments:
    - `file`:
    - `test_url`:
    """
    return V.validate_proxies(get_all_proxies(file), test_url)[0]
    
