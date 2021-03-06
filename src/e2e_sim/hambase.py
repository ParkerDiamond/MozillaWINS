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

        self.latencies = []
        self.n_misses = 0
        self.n_hits = 0
        self.n_dropped = 0
        self.n_served = 0
        self.n_reqs = 0
        self.retransmits = 0


    def round_init(self):
        self.round_txd_rxd = 0

    def round_end(self):
        results_file = self.sim.config.results_file

        with open(results_file, 'a') as f:
            f.write('{},{},{},{},{}\n'.format(self.round_txd_rxd,
                                            (self.n_hits / self.n_reqs),
                                            (self.n_dropped / self.n_reqs),
                                            (self.retransmits / self.n_reqs),
                                            sum(self.latencies) / self.n_served))

        print('[RESULT] hambase bytes txd_rxd: {}'.format(self.round_txd_rxd))
        print('[RESULT] hit rate: {:f}'.format(self.n_hits / self.n_reqs))
        print('[RESULT] drop rate: {:f}'.format(self.n_dropped / self.n_reqs))
        print('[RESULT] retransmit rate: {:f}'.format(self.retransmits / self.n_reqs))
        print('[RESULT] avg latency: {:f}'.format(sum(self.latencies) / self.n_served))


    def generate_request(self, site):
        'generate a semi-realistic HTTP request'
        return '''GET / HTTP/1.1
Host: {}
User-Agent: Some agent

'''.format(site)


    def fetch_site(self, client, site):
        '''returns latency for a request from a client (not including LAN latency)'''
        self.n_reqs += 1

        bpr = self.bandwidth * self.sim.config.round_length
        if self.round_txd_rxd > bpr:
            self.n_dropped += 1
            return None

        total_txd = 0
        total_rxd = 0

        if site in self.cached:
            # should be almost 0
            latency = self.sim.config.cache_latency
            self.n_hits += 1
        else:
            self.n_misses += 1

            req_data = self.generate_request(site)
            resp_data, net_latency = self.netbase.fetch_site(site)

            latency = net_latency
            while True:
                success, txd = radio.attempt_transmission(req_data, self.tx_error)
                total_txd += txd
                latency += self.sim.config.one_way_latency + (txd / self.bandwidth)

                if success:
                    success, rxd = radio.attempt_transmission(resp_data, self.rx_error)
                    total_rxd += rxd
                    latency += self.sim.config.one_way_latency + (rxd / self.bandwidth)
                    if success:
                        break
                    else:
                        self.retransmits += 1
                        latency += self.retransmit_delay
                else:
                    self.retransmits += 1
                    latency += self.retransmit_delay

            total_bs = total_rxd + total_txd
            self.round_txd_rxd += total_bs

            bpr = self.bandwidth * self.sim.config.round_length
            if self.round_txd_rxd > bpr:
                # if we use all our bandwidth for a round, drop the request
                print('total bandwidth exceeded in round: {}/{}'.format(self.round_txd_rxd, bpr))
                self.n_dropped += 1
                return None

        self.cache(site)

        print('got {} for client {} in {:.3f}s. {} rxd {} txd'.format(site, client.id_num, latency, total_rxd, total_txd))
        self.n_served += 1
        self.latencies.append(latency)

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


