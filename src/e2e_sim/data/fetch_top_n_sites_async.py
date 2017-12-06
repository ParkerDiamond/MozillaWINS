#!/usr/bin/env python


import csv
import sys
import pickle
import requests
import asyncio

class Site:
    def __init__(self, rank, domain, popularity_subnets, popularity_ips):
        self.rank = rank
        self.domain = domain
        self.popularity_subnets = popularity_subnets
        self.popularity_ips = popularity_ips
        self.pop = self.popularity_subnets

def load_sites(sites_file, sites_to_load):
    full_sites = dict()

    with open(sites_file, 'r') as top_sites:
        reader = csv.DictReader(top_sites)
        for i, row in enumerate(reader):
            if i > sites_to_load:
                break

            rank = int(row['GlobalRank'])
            sitename = str(row['Domain'])
            popularity_subnets = int(row['RefSubNets'])
            popularity_ips = int(row['RefIPs'])

            existing_site = full_sites.get(sitename)
            if not existing_site:
                site = Site(rank, sitename, popularity_subnets, popularity_ips)
                full_sites[sitename] = site

    return full_sites



cached_sites = []


def fetch_site(i, sitename, site):
    global cached_sites

    print("Caching site {}".format(i))
    url = 'http://' + sitename
    response = requests.get(url, timeout=1)
    latency = response.elapsed.total_seconds()
    cached_sites.append((sitename, site.pop, latency, response.content))

def main():
    sites_file = str(sys.argv[1])
    sites_to_load = int(sys.argv[2])

    full_sites = load_sites(sites_file, sites_to_load)
    cached_sites = list()

    loop = asyncio.get_event_loop()
    for i, (sitename, site) in enumerate(full_sites.items()):
        loop.run_in_executor(None, fetch_site, i, sitename, site)

    f = open('cached_{}_sites.p'.format(sites_to_load), 'wb')
    pickle.dump(cached_sites, f)
    f.close()


if __name__ == '__main__':
    main()
