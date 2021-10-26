#!/usr/bin/python

"""MPTCP Demo"""

from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import WirelessLink
import os

def topology():

 

    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation(
        'sta1', wlans=2, ip='10.0.0.10/8', position='51,10,0', range=10 )
    ap2 = net.addAccessPoint(
        'ap2', mac='00:00:00:00:00:02',
        protocols='OpenFlow13', ssid= 'ssid_ap2', mode= 'g',
        channel= '6', position='55,17,0', band='5', range=30 )
    ap3 = net.addAccessPoint(
        'ap3', mac='00:00:00:00:00:03',
        protocols='OpenFlow13', ssid= 'ssid_ap3', mode= 'g',
        channel= '1', position='50,11,0', range=10 )
    h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.254/8')
    h5 = net.addHost( 'h5', mac='00:00:00:00:00:05', ip='192.168.0.254/24')
    h10 = net.addHost( 'h10', mac='00:00:00:00:00:10', ip='192.168.1.2/24' )
    c1 = net.addController( 'c1', controller=RemoteController, ip='192.168.100.113' )
    # host dummy
    sta2 = net.addStation('sta2', ip='10.0.0.11/8', position='55,10,0', range=10 )
    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap2, sta1, 0, 0)
    net.addLink(ap3, sta1, 0, 1)
    net.addLink(ap2, h4,bw=1000)
    net.addLink(ap3, h5,bw=1000)
    net.addLink(h4, h10 )
    net.addLink(h5, h10)
    
    net.addLink(sta2,ap2)
    h4.cmd('ifconfig h4-eth1 192.168.1.1/24')
    h5.cmd('ifconfig h5-eth1 192.168.2.1/24')

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10/8')
    sta1.cmd('ifconfig sta1-wlan1 192.168.0.10/24')

    
    # config ip h10
    h10.cmd('ifconfig h10-eth1 192.168.2.2/24')

    #sta1.cmd('ip route add 10.0.0.0/24 dev sta1-wlan0 scope link table 1')
    #sta1.cmd('ip route add 192.168.0.0/24 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add 192.168.2.0/24 via 192.168.0.254')
    sta1.cmd('ip route add 192.168.1.0/24 via 10.0.0.254')  

    sta1.cmd('ip rule add from 10.0.0.10 table 1')
    sta1.cmd('ip rule add from 192.168.0.10 table 2')
    sta1.cmd('ip route add 10.0.0.0/24 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 192.168.0.0/24 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-wlan1 table 2')
    sta1.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta1-wlan0')

    #host background
    sta2.cmd('ip rule add from 10.0.0.11 table 1')
    sta2.cmd('ip route add 10.0.0.0/24 dev sta2-wlan0 scope link table 1')
    sta2.cmd('ip route add default via 10.0.0.254 dev sta2-wlan0 table 1')
    sta2.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta2-wlan0')

    net.plotGraph()

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap2.start( [c1] )
    ap3.start( [c1] )

    #h10.cmd('ip route add 10.0.0.0/8 via 192.168.1.1')
    #h10.cmd('ip route add 192.168.0.0/24 via 192.168.1.2')

    h10.cmd('ip rule add from 192.168.1.2 table 1')
    h10.cmd('ip rule add from 192.168.2.2 table 2')    
    h10.cmd('ip route add 192.168.1.0/24 dev h10-eth0 scope link table 1')
    h10.cmd('ip route add default via 192.168.1.1 dev h10-eth0 table 1')  
  
    h10.cmd('ip route add 192.168.2.0/24 dev h10-eth1 scope link table 2')
    h10.cmd('ip route add default via 192.168.2.1 dev h10-eth1 table 2')
    h10.cmd('ip route add default scope global nexthop via 192.168.1.1 dev h10-eth0')
    h4.cmd('sysctl -w net.ipv4.ip_forward=1')
    h5.cmd('sysctl -w net.ipv4.ip_forward=1')

    sta1.cmdPrint('tc qdisc del dev sta1-wlan0 root')
    sta1.cmdPrint('tc qdisc del dev sta1-wlan1 root')
    
    sta1.cmdPrint('tc qdisc add dev sta1-wlan0 root netem limit 3Mbit loss 1% delay 75ms')
    sta1.cmdPrint('tc qdisc add dev sta1-wlan1 root netem limit 5Mbit loss 2% delay 10ms')
    
    info("*** Running CLI\n")
    CLI( net )
    
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    os.system('mn -c')
    os.system('modprobe mptcp_balia && sysctl -w net.ipv4.tcp_congestion_control=balia')
    #os.system('modprobe mptcp_balia && sysctl -w net.ipv4.tcp_congestion_control=olia')
    #os.system('modprobe mptcp_coupled && sysctl -w net.ipv4.tcp_congestion_control=lia') 
    #os.system('modprobe mptcp_balia && sysctl -w net.ipv4.tcp_congestion_control=wvegaz')
    setLogLevel( 'info' )
    topology() 
