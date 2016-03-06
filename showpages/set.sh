#!/bin/bash

sysctl -w net.ipv4.ip_forward=1

echo 0 | sudo tee /proc/sys/net/ipv4/conf/eth0/send_redirects

iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080

iptables -t nat -L --line-numbers

#iptables -t nat -D PREROUTING 1