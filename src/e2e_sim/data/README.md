# Simulation Data

- `majestic_million.csv`: The top 1 million sites on the Internet ranked by the number of referring subnets, roughly approximating the Alexa Top 1 million, whose data costs money.
- `cached_10000_sites.p`: A pickled Python object in the format: `[(sitename - str, popularity - int, latency - float, homepage content - bytes), (...), ...]` that covers the top 10,001 sites from the majestic million dataset. If a site was not able to be fetched in 1 second, then the tuple will look like `(sitename - str, None, None, None)`.
