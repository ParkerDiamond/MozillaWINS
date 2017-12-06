# Simulation Data


## Data Files
- `majestic_million.csv`: The top 1 million sites on the Internet ranked by the number of referring subnets, roughly approximating the Alexa Top 1 million, whose data costs money.
- `cached_10000_sites.p`: A pickled Python object in the format: `[(sitename - str, popularity - int, latency - float, homepage content - bytes), (...), ...]` that covers the top 10,001 sites from the majestic million dataset. If a site was not able to be fetched in 1 second, then the tuple will look like `(sitename - str, None, None, None)`.

## Scripts
- `fetch_top_n_sites.py`: This pulls the top `n` sites data. The usage is `./fetch_top_n_sites.py majestic_million.csv 1000` where 1000 can be replaced for any other value of `n` up to 999,999 (which is the number of sites in the majestic million data).

## Data Sources
- The Majestic Million comes from https://majestic.com/reports/majestic-million and https://blog.majestic.com/development/majestic-million-csv-daily/.
