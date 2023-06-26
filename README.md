# Licensing Server
A simple licensing server with an optional Pterodactyl Egg

This is designed to be run through a Cloudflare Tunnel or Proxy and it requires a MariaDB Database.
This only reads from the database, it does not insert data into it; you will have to use another program for that or do it manually.
This uses (Robyn)[https://github.com/sparckles/robyn], a python webserver that uses a Rust Runtime for better performance.

When hosting this in Pterodactyl Panel, you have several options for exposing it. You can allocate the internal address of your
public internet interface and send requests to public_ip:port, you can allocate the internal ip of your pterodactyl0 interface
and use a Cloudflare Tunnel proxying http (Cloudflare will handle the encryption) and pointing to 172.18.0.1:container_port like I have in testing.
If you allocate 127.0.0.1 Wings will automatically read that as the internal IP of your pterodactyl interface, by default 172.18.0.1

Here's an example of a CURL request you can use when testing (Make sure to set DEBUG to true for verbose information):
```
curl -X POST -H "Content-Type: application/json" -d '{"license_key":"test"}' https://subdomain-for-your-tunnel.domain.com
```

The egg's install script creates a database with columns for license as the primary key and ip which are both requires as well as discordid and email which can be NULL.
It also creates a view that just sees license and ip and uses that for checking.

If the license exists and the IP that goes with that license matches the IP the request was sent from the server will return status: success and message: License verified.
If not, it will return status: failure and message: License not found or IP mismatch.

When modifying this program to suit your application's needs, some useful information can be found at the following links:
- https://robyn.tech/
- https://man.archlinux.org/man/extra/mariadb-clients/mariadb.1.en
