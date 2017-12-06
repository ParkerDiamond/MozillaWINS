"""
    HAM side client
"""

import random

import numpy as np

class Client:
    def __init__(self, sim, id_num):
        self.id_num = id_num
        self.sim = sim
        self.results = []
        self.request_rate = self.sim.config.client_request_rate

    def update_round(self):
        # TODO allow multiple requests per round?
        # OR no requests per round?
        # ^ these are both definitely good ideas

        n_requests = np.random.poisson(self.request_rate * self.sim.config.round_length)
        
        for _ in range(n_requests):
            site = self.sim.random_site()

            result = self.sim.hambase.fetch_site(self, site)

            if result is not None:
                latency, txd, rxd = result
            else:
                latency = None

            self.results.append((site, latency))

                
