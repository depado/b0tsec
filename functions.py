#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import urllib.request
import urllib.parse
import json
# import os
# import nude

def shorten(url):
    if not "http://" in url:
        url = "http://{}".format(url)
    values = {
        'longUrl': url,
        'login': "depado",
        'apiKey': "R_08737c502c7cab490523a7033f4f951c",
        'format': 'json'
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request("http://api.bit.ly/v3/shorten", data)
    try:
        try:
            response = self.opener.open(request)
        except Exception as e:
            return False
        else:
            short = json.loads(response.read().decode("utf-8"))['data']['url']
            return short

    except Exception as e:
        return False

# def check_sanity(url):
#     try:
#         local_filename, headers = urllib.request.urlretrieve(url)
#         nudity = nude.is_nude(local_filename)
#         os.remove(local_filename)
#         return nudity
#     except Exception as e:
#         print(e)
