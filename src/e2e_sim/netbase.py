"""
    Internet-connected base station
"""


import cache


class NetBase:
    """
        Internet base station class
    """

    def __init__(self, sim):
        """
            Initialize the NetBase class
        """
        self.sim = sim
        self.cache = cache.Cache('data/cached_10000_sites.p')

    def fetch_site(self, site):
        """
            Take sitename and either return the cached content or make the request, cache the site, then return the content
        """
        cached_site = self.cache.get_site(site)
        if cached_site:
            return cached_site.content, cached_site.latency
        else:
            raise ValueError('Invalid site requested: {}'.format(site))
            url = 'http://' + site
            response = requests.get(url)
            latency = response.elapsed.total_seconds()
            self.cache.cache_site(site, response.content, latency)
            return response.content, latency

