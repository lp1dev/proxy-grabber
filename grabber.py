#!/bin/python

import re
import asyncio
import json
import concurrent.futures
import requests
from searx.api import search

THREADS=10
FILE_TYPES="txt"

def     get_from_cache():
  with open("cache/results.json") as f:
    return json.loads(f.read())

def     run(files, max_workers=THREADS):
  with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    loop = asyncio.get_event_loop()
    futures = loop.run_in_executor()
#    for response in await asyncio.gather(*futures):
#      pass
  return 0

def     get_proxies(files):
  proxies = []
  for f in files:
    r = requests.get(f)
    if r.status_code == 200:
      items = r.text.split()
      for item in items:
        if re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\:?([0-9]{1,5})?", item):
          proxies.append(item)
    return proxies

def     seek_proxy_files(url):
  files = []
  r = requests.get(url)
  ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
  if r.status_code == 200:
    for match in re.finditer(ultimate_regexp, r.text):
      group = match.group()
      if "<a" in group and ".%s" %FILE_TYPES in group:
        if "://" in group:
          files.append("%s" %(group.replace("<a href=\"", '')[:-2]))
        else:
          files.append("%s%s" %(url, group.replace("<a href=\"", '')[:-2]))
    return files

def     walk_results(results):
  files = []
  for result in results:
    print('Seeking files in ', result['url'])
    files += seek_proxy_files(result['url'])
  print('Found %i potential files' %(len(files)))
  return files
      
def     seek_proxies(): 
  status, content = search('intitle:"index of" +"last modified" +"parent directory" +(%s) proxy list' %FILE_TYPES)
  if status is False:
    print(content)
    content = get_from_cache()
  files = walk_results(content['results'])
  proxies = get_proxies(files)
  print("Found %i proxies" %(len(proxies)))
  return proxies

def     main():
  print(seek_proxies())

if __name__ == '__main__':
  main()
