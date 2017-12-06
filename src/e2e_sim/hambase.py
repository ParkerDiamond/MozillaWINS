import radio

class HamBase:
    def __init__(self, sim, netbase, clients):
        self.sim = sim
        self.netbase = netbase
        self.clients = clients

        self.max_cache = self.sim.config.max_cache
        self.cached = {}
        self.cache_n = 0
        self.round_txd_rxd = 0
        self.bandwidth = self.sim.config.ham_bandwidth
        self.retransmit_delay = self.sim.config.ham_retransmit_delay


    def round_init(self):
        self.round_txd_rxd = 0

    def fetch_site(self, client, site):
        '''returns latency for a request from a client (not including LAN latency)'''

        if site in self.cached:
            # should be almost 0
            return self.sim.config.cache_latency

        req_data = self.generate_request(site)
        resp_data = self.netbase.fetch_site(site)

        total_txd = 0
        total_rxd = 0
        latency = 0
        while True:
            attempts += 1
            success, txd = radio.attempt_transmission(req_data, error)
            total_txd += txd
            latency += self.sim.config.one_way_latency

            if success:
                success, rxd = radio.attempt_transmission(resp_data, error)
                total_rxd += rxd
                latency += self.sim.config.one_way_latency
                if success:
                    break
            else:
                latency += self.retransmit_delay

        self.round_txd_rxd += total_txd + total_rxd

        if self.round_txd_rxd > self.bandwidth * self.sim.config.round_length:
            # if we use all our bandwidth for a round, drop the request
            return None

        self.cache(site)

        return latency, total_txd, total_rxd

    def cache(self, site):
        # TODO other caching policies?

        cache = self.cached.items()
        lru = min(self.cached.items(), key=lambda x: x[1])
        lru_site = lru[0]
        del self.cached[lru_site]

        self.cache_n += 1
        self.cached[site] = self.cache_n














