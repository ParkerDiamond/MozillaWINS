import radio

class HamBase:
    def __init__(self, sim):
        self.sim = sim
        self.netbase = sim.netbase

        self.max_cache = self.sim.config.max_cache
        self.cached = {}
        self.cache_n = 0
        self.round_txd_rxd = 0
        self.bandwidth = self.sim.config.ham_bandwidth
        self.tx_error = self.sim.config.tx_error
        self.rx_error = self.sim.config.rx_error
        self.retransmit_delay = self.sim.config.ham_retransmit_delay


    def round_init(self):
        self.round_txd_rxd = 0

    def round_end(self):
        print('hambase bytes txd_rxd: {}'.format(self.round_txd_rxd))

    def generate_request(self, site):
        'generate a semi-realistic HTTP request'
        return '''GET / HTTP/1.1
Host: {}
User-Agent: Some agent

'''.format(site)


    def fetch_site(self, client, site):
        '''returns latency for a request from a client (not including LAN latency)'''

        total_txd = 0
        total_rxd = 0

        if site in self.cached:
            # should be almost 0
            latency = self.sim.config.cache_latency
        else:
            req_data = self.generate_request(site)
            resp_data, net_latency = self.netbase.fetch_site(site)

            latency = net_latency
            while True:
                success, txd = radio.attempt_transmission(req_data, self.tx_error)
                total_txd += txd
                latency += self.sim.config.one_way_latency

                if success:
                    success, rxd = radio.attempt_transmission(resp_data, self.rx_error)
                    total_rxd += rxd
                    latency += self.sim.config.one_way_latency
                    if success:
                        break
                else:
                    latency += self.retransmit_delay

            total_bs = total_rxd + total_txd
            self.round_txd_rxd += total_bs

            bpr = self.bandwidth * self.sim.config.round_length
            if self.round_txd_rxd > bpr:
                # if we use all our bandwidth for a round, drop the request
                print('total bandwidth exceeded in round: {}/{}'.format(self.round_txd_rxd, bpr))
                return None

        self.cache(site)

        print('got {} for client {} in {}s. {} rxd {} txd'.format(site, client.id_num, latency, total_rxd, total_txd))

        return latency, total_txd, total_rxd

    def cache(self, site):
        # TODO other caching policies?

        while len(self.cached) >= self.max_cache:
            cache = self.cached.items()
            lru = min(self.cached.items(), key=lambda x: x[1])
            lru_site = lru[0]
            del self.cached[lru_site]

        self.cache_n += 1
        self.cached[site] = self.cache_n


