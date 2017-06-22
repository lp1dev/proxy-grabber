import requests
import concurrent.futures
import asyncio
import time

results = []

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

async def loop_test_proxies(proxies, timeout, threads):
    global results
    url = "https://monip.org"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        loop = asyncio.get_event_loop()
        futures = []
        for proxy in proxies:
            futures.append(loop.run_in_executor(executor, test_proxy, url, proxy, timeout))
        for response in await asyncio.gather(*futures):
            if response is not None:
                results.append(response)
            pass


def test_proxies(proxies, timeout, threads):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_test_proxies(proxies, timeout, threads))
    return results
