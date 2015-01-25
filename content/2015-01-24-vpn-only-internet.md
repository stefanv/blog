Title: VPN-only access to the internet
Tags: linux
Status: published

tl;dr A firewall setup that allows traffic to leave *only* via the VPN

A few days ago, I noticed that my outbound email wasn't being
delivered---it seems as if my ISP blocks access to some outbound ports.
An easy workaround is to route traffic through the work VPN, but
knowing myself I'd forget to switch it on, leaving my outbound mail
stranded.

I needed a way of blocking *any* access to the internet, unless it was
leaving through the VPN (since I was sure I'd notice *that* pretty
quickly).

I'd have preferred to use firewalld, which is neatly integrated into
Ubuntu, but as of 01/24/2015 it 
[doesn't allow filtering outbound traffic](https://lists.fedorahosted.org/pipermail/firewalld-users/2014-October/000250.html)[^firewalld_direct_zones]. What
follows, then, is a simple approach implementing the following rule:

 > Block wifi traffic unless it goes to either the local
 > network or the VPN.

Create a script (I called it ``~/scripts/fw-up``) that sets up the
firewall:

```bash
#!/bin/bash

# Clear any existing rules
iptables -F

# Allow outbound DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT

# Allow TCP access to the work VPN
# Replace X.Y below with your VPN address range
iptables -A OUTPUT -p tcp -d X.Y.0.0/16 -o wlan1 -j ACCEPT

# Allow any traffic destined for the vpn to go out
iptables -A OUTPUT -o vpn0 -j ACCEPT

# Allow local traffic
iptables -A OUTPUT -p tcp -o wlan1 -d 10.0.0.0/8 -j ACCEPT
iptables -A OUTPUT -p tcp -o wlan1 -d 172.16.0.0/12 -j ACCEPT
iptables -A OUTPUT -p tcp -o wlan1 -d 192.168.0.0/16 -j ACCEPT

# Drop everything else on the wifi
iptables -A OUTPUT -p tcp -o wlan1 -j DROP
```

Make sure the script is set to executable (``chmod +x fw-up``).

Add a symlink to ``if-up.d`` to ensure that the firewall gets built
whenever the network is reconfigured:

```
sudo ln -s ~/scripts/fw-up /etc/network/if-up.d/iptables
```

Now, whenever you connect to a wifi hotspot, internet traffic will be
blocked until you fire up your VPN.  If, on occasion, you need to work
without the VPN, simply raze the firewall:

```
sudo iptables -F
```


[^firewalld_direct_zones]: The idea would be to set up a zone, say
`vpn_only`, and to assign your home wifi SSID to it.  A direct rule that
blocks any non-VPN traffic can then be added to the new zone (this
should be possible soon, and is on the firewalld
[TODO list](https://git.fedorahosted.org/cgit/firewalld.git/tree/TODO).

<!---
# Create a new zone

**Direct rules not supported for zones yet**



``sgs3``

```
sudo firewall-cmd --permanent --new-zone=vpn_only
sudo firewall-cmd --reload
```

In NetworkManager, go to the wifi connection and set its zone to
``vpn_only``.

(Alternatively, directly edit
``/etc/NetworkManager/system-connections/<ssid>``)


Restart NetworkManager:

```
$ sudo service network-manager restart
```

When your connection comes back up, you should see it in the new zone:

```
sudo firewall-cmd --zone=vpn_only --list-interfaces
```

Firewalld has a *direct* mode which gives us access to the inner
workings of the firewall, among other things allowing us to manipulate
outgoing and IP-based rules.

sudo firewall-cmd --zone=vpn_only --permanent --add-rich-rule='rule family="ipv4" destination address="136.152.0.0/16" invert="True" port port="1-65535" protocol="tcp" reject'

rule family="ipv4" destination NOT address="136.152.0.0/16" port
port="1-65535" protocol="tcp" reject
-->
