import random

class Client:
    def __init__(self, sim, hambase):
        self.sim = sim
        self.hambase = hambase

    def update_round(self):
        site = random.choice(self.sim.config.sites)

        # TODO allow multiple requests per round?
        # OR no requests per round?
        # ^ these are both definitely good ideas

        latency = self.hambase.request(self, site)


        
        
        
