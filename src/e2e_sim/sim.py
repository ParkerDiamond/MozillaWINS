"""
    Simulation Framework
"""


# Python Standard Library
import argparse
import csv
import random

# Local modules
import hambase
import netbase
import client

# 3rd Party Libraries
import anyconfig
import requests


class SimulationConfig:
    """
        Config class for the simulation
    """

    def __init__(self):
        self.config_dict = None

    def load_config(self, config_file):
        self.config_dict = anyconfig.load(config_file, ac_parser="yaml")
        for k, v in self.config_dict.items():
            setattr(self, k, v)


class Site:
    def __init__(self, rank, domain, popularity_subnets, popularity_ips):
        self.rank = rank
        self.domain = domain
        self.popularity_subnets = popularity_subnets
        self.popularity_ips = popularity_ips
        self.pop_rank = self.popularity_subnets


class Simulation:
    """
        Main simulation class
    """

    def __init__(self, config_file):
        self.config = SimulationConfig()
        self.config.load_config(config_file)

        self.full_sites = dict()
        self.sites = []
        self.load_sites()

        self.netbase = netbase.NetBase(self)

        num_clients = self.config.num_clients
        if not isinstance(num_clients, int):
            raise ValueError('Number of clients in config file is not an integer!')

        self.clients = []
        for client_num in range(num_clients):
            self.clients.append(client.Client(self, client_num))

        self.hambase = hambase.HamBase(self)

    def load_sites(self):
        with open(self.config.top_sites_file, 'r', encoding='utf-8') as top_sites:
            reader = csv.DictReader(top_sites)
            for i, row in enumerate(reader):
                if i > self.config.sites_to_load:
                    break

                rank = int(row['GlobalRank'])
                sitename = str(row['Domain'])
                popularity_subnets = int(row['RefSubNets'])
                popularity_ips = int(row['RefIPs'])

                existing_site = self.full_sites.get(sitename)
                if not existing_site:
                    site = Site(rank, sitename, popularity_subnets, popularity_ips)
                    self.full_sites[sitename] = site
                    self.sites.append((sitename, popularity_subnets))

    def print_config(self):
        print("Simulation config:")
        print("{}".format(self.config.config_dict))

    def random_site(self):
        while True:
            # First element is domain without protocol, second is popularity
            site = random.choice(list(self.netbase.cache.cache))
            try:
                self.netbase.fetch_site(site)
            except requests.RequestException:
                self.sites.remove(site)
            else:
                return site

    def run_round(self, round_num):
        print("Running round number {}!".format(round_num))
        self.hambase.round_init()

        for c in self.clients:
            c.update_round()


def setup_argparser():
    """
        Setup argument parser
    """
    parser = argparse.ArgumentParser(description='End-to-End SARATOGA Simulation Framework')
    parser.add_argument("-c", "--config", dest='config', type=str, default='config.yml', help="Config filename")
    parser.add_argument("-nr", "--num-rounds", dest='num_rounds', type=int, default=1000, help="Number of rounds to run")
    return parser


def main():
    # Parse CLI arguments
    parser = setup_argparser()
    args = parser.parse_args()

    # Setup simulation framework
    sim = Simulation(args.config)

    # Show simulation config
    sim.print_config()

    # Run every round of the simulator
    for round_num in range(args.num_rounds):
        sim.run_round(round_num)


if __name__ == '__main__':
    main()
