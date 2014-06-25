#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import urllib.request
import urllib.parse
import json


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


def periodic_task(interval, times = -1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap