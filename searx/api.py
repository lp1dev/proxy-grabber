#!/usr/bin/python

import requests
import json

ENGINE_URL="https://searx.me/?q=%s&categories=%s&format=%s"



def search(query, fmt="json", categories="general"):
    r = requests.get(ENGINE_URL %(query, categories, fmt))
    if r.status_code == 200:
        print(r.text)
        return True, json.loads(r.text)
    return False, {"error": r.text, "code": r.status_code}

def main():
    print(search('search engine'))
    return 0

if __name__ == "__main__":
    exit(main())
