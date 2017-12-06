
class HamBase:
    def __init__(self, sim, netbase, clients):
        self.sim = sim
        self.netbase = netbase
        self.clients = clients

        self.max_cache = self.sim.config.max_cache
        self.cached = {}
        self.cache_n = 0


    def fetch_site(self, client, site):
        '''returns latency for a request from a client (not including LAN latency)'''

        if site in self.cached:
            # should be almost 0
            return self.sim.config.CACHE_LATENCY

        req_data = self.generate_request(site)

        req_latency = 0

        attempts = 1
        while not attempt_transmission(req_data):
            attempts += 1

        resp_latency = self.netbase.fetch_site(site)

        self.cache(site)

        return req_latency + resp_latency

    def cache(self, site):
        # TODO other caching policies?

        cache = self.cached.items()
        lru = min(self.cached.items(), key=lambda x: x[1])
        lru_site = lru[0]
        del self.cached[lru_site]

        self.cache_n += 1
        self.cached[site] = self.cache_n














