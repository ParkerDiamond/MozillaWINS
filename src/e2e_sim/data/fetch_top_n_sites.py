#!/usr/bin/env python


import csv
import sys
import pickle
import requests
import multiprocessing as mp

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


def fetch_site(i, sitename, site):
    print("Caching site {}".format(i))
    url = 'http://' + sitename
    try:
        response = requests.get(url, timeout=1)
    except Exception:
        return (sitename, None, None, None)
    latency = response.elapsed.total_seconds()
    return (sitename, site.pop, latency, response.content)

def main():
    sites_file = str(sys.argv[1])
    sites_to_load = int(sys.argv[2])

    full_sites = load_sites(sites_file, sites_to_load)
    cached_site_results = list()

    pool = mp.Pool()
    for i, (sitename, site) in enumerate(full_sites.items()):
        cached_site_results.append(pool.apply_async(fetch_site, (i, sitename, site,)))
    pool.close()
    pool.join()

    cached_sites = []
    for cs in cached_site_results:
        cached_sites.append(cs.get())

    f = open('cached_{}_sites.p'.format(sites_to_load), 'wb')
    pickle.dump(cached_sites, f)
    f.close()


if __name__ == '__main__':
    main()
