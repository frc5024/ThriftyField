echo "Setting up wifi"
sudo nano /etc/dhcpcd.conf
sudo service dhcpcd restart

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  
echo "interface=wlan0" > /etc/dnsmasq.conf
echo "dhcp-range=10.10.100.2,10.10.100.20,255.255.255.0,24h" >> /etc/dnsmasq.conf


echo "interface=wlan0" >> /etc/hostapd/hostapd.conf
echo "driver=nl80211" >> /etc/hostapd/hostapd.conf
echo "ssid=FieldNet" >> /etc/hostapd/hostapd.conf
echo "hw_mode=g" >> /etc/hostapd/hostapd.conf
echo "channel=7" >> /etc/hostapd/hostapd.conf
echo "wmm_enabled=0" >> /etc/hostapd/hostapd.conf
echo "macaddr_acl=0" >> /etc/hostapd/hostapd.conf
echo "auth_algs=1" >> /etc/hostapd/hostapd.conf
echo "ignore_broadcast_ssid=0" >> /etc/hostapd/hostapd.conf
echo "wpa=2" >> /etc/hostapd/hostapd.conf
echo "wpa_passphrase=5k24ThriftyField" >> /etc/hostapd/hostapd.conf
echo "wpa_key_mgmt=WPA-PSK" >> /etc/hostapd/hostapd.conf
echo "wpa_pairwise=TKIP" >> /etc/hostapd/hostapd.conf
echo "rsn_pairwise=CCMP" >> /etc/hostapd/hostapd.conf

sudo nano /etc/default/hostapd

sudo systemctl start hostapd
sudo systemctl start dnsmasq

sudo nano /etc/sysctl.conf

sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

sudo nano /etc/rc.local
sudo reboot
