# Layout

HamBase - HAM base station, conected to client via LAN, and NetBase over radio

NetBase - HAM base station connected to internet

Client - Off the grid people


```
Client 1 ----
             \
Client 2 -------[LAN]------ HamBase ----[Radio]-----NetBase------Internet
             /
Client 3 ----
```

Variable number of clients

Clients will randomly request one of the top sites - selected based off of acutal traffic (e.g. most popular site gets requested most often)

HamBase has a cache of configurable size. If the site is cached, then assume client gets it with LAN latency (LAN latency is some small constant)

On cache miss, HamBase fetches site from NetBase. We will generate a realistic HTTP request for the site, compress and encode it, then apply random errors. We will then test decoding and uncompressing. Repeat until success. NetBase class will then actually fetch the site's homepage, compress and encode it, and apply random errors again. Test with retransmission again. Also simulate ACKS?
