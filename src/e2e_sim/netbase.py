"""
    Internet-connected base station
"""


import requests


class Site:
    def __init__(self, sitename, content, latency):
        """
            Create a site instance
        """
        self.sitename = sitename
        self.content = content
        self.latency = latency


class Cache:
    def __init__(self):
        """
            Initialize the internal cache dictionary
        """
        self.cache = dict()

    def get_site(self, sitename):
        """
            If site is cached return the cached sitem otherwise return None
        """
        cached = self.cache.get(sitename)
        if cached:
            return cached
        else:
            return None

    def cache_site(self, sitename, content, latency):
        """
            Cache a site in the internal cache dictionary
        """
        site = Site(sitename, content, latency)
        self.cache[sitename] = site_object
        return site


class NetBase:
    """
        Internet base station class
    """

    def __init__(self):
        """
            Initialize the NetBase class
        """
        self.cache = Cache()

    def fetch_site(site):
        """
            Take sitename and either return the cached content or make the request, cache the site, then return the content
        """
        cached_site = self.cache.get_site(site)
        if cached_site:
            return cached_site.content
        else:
            response = requests.get(site)
            self.cache.cache_site(site, response.content, response.elapsed)
            return response.content
