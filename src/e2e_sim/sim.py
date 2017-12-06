"""
    Simulation Framework
"""

# Python Standard Library
import argparse

# Local modules
import hambase
import netbase
import client

# 3rd Party Libraries
import anyconfig

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


class Simulation:
    """
        Main simulation class
    """

    def __init__(self, config_file):
        self.config = SimulationConfig()
        self.config.load_config(config_file)

        self.netbase = netbase.NetBase()

        num_clients = self.config.num_clients
        if not isinstance(num_clients, int):
            raise ValueError('Number of clients in config file is not an integer!')

        self.clients = []
        for client_num in range(num_clients):
            self.clients.append(client.Client(self))

        self.hambase = hambase.HamBase(self, self.netbase, self.clients)

    def print_config(self):
        print("Simulation config:")
        print("{}".format(self.config))

    def run_round(self, round_num):
        print("Running round number {}!".format(round_num))


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
