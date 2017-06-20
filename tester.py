import requests
import time

def test_proxy(url, proxy, timeout):
    http_proxy  = "http://%s" %proxy
    https_proxy = "https://%s" %proxy
    ftp_proxy   = "ftp://%s" %proxy
    proxyDict = { 
              "http"  : http_proxy,
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }
    try:
        print("Testing proxy %s" %proxy)
        s = requests.Session()
        start = time.time()
        r = s.get(url, proxies=proxyDict, timeout=timeout)
        end = time.time()
        print("Proxy seems UP !\nAnswered in : %s" %(end-start))
        if "detected" in r.text:
            return {"success": "proxy answered in %s" %(end-start), "time": end-start, "detected": True}
        else:
            return {"success": "proxy answered in %s" %(end-start), "time": end-start, "detected": False}
    except Exception as e:
        print(e)
        return {"error": "Proxy down", "code": 2}

def test_proxies(proxies, timeout):
    results = []
    url = "https://monip.org"
    for proxy in proxies:
        results.append(test_proxy(url, proxy, timeout))
    return results
