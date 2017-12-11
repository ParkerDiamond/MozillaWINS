#!/usr/bin/env python

import copy
import os
import sys
import subprocess
import multiprocessing as mp

import anyconfig


def run_param_test(config_string):
    subprocess.run(['python', 'sim.py', '-cs', str(config_string)], check=True)


def main():
    params_file = None
    if len(sys.argv) < 4:
        print('Usage: python test.py TEST_PARAMS_FILE DEFAULT_CONFIG_FILE NUM_ROUNDS')
        sys.exit(1)
    else:
        params_file = str(sys.argv[1])
        default_config = str(sys.argv[2])
        num_rounds = int(sys.argv[3])

    variable_params = anyconfig.load(params_file)
    default_config = anyconfig.load(default_config)

    configs = []
    for k, v in variable_params.items():
        if v is not None:
            options = v
            for option in options:
                new_config = copy.deepcopy(default_config)
                new_config[k] = option
                str_option = str(option)
                new_config['results_file'] = 'results_{}_{}.txt'.format(k, str_option.replace('.', '_'))
                new_config['num_rounds'] = num_rounds
                cs = anyconfig.dumps(new_config, ac_parser='yaml')
                configs.append(cs)

    pool = mp.Pool(processes=48)
    for config_str in configs:
        pool.apply_async(run_param_test, (config_str,))
    pool.join()


if __name__ == '__main__':
    main()
