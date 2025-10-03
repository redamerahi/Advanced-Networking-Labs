#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""
"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

"Function definition: This is called from the main function"
def firstNetwork():

    "Create an empty network and add nodes to it."
    net = Mininet()
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    PC1 = net.addHost( 'PC1', ip='10.10.10.1/24')
    PC2 = net.addHost( 'PC2', ip='10.10.20.2/24')
    PC3 = net.addHost( 'PC3', ip='10.10.30.3/24')
    PC4 = net.addHost( 'PC4', ip='10.10.10.4/24')
    
    info( '*** Adding switch\n' )
    s14 = net.addSwitch( 's14' )
    s24 = net.addSwitch( 's24' )
    s34 = net.addSwitch( 's34' )

    
    info( '*** Creating links\n' )
    net.addLink( PC1, s14 )
    net.addLink( PC2, s24 )
    net.addLink( PC3, s34 )

    net.addLink( PC4, s14)
    net.addLink( PC4, s24)
    net.addLink( PC4, s34)

    PC4.cmd('ip addr add 10.10.20.4/24 dev PC4-eth1')
    PC4.cmd('ip addr add 10.10.30.4/24 dev PC4-eth2')
    PC4.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    info( '*** Starting network\n')
    net.start()

    PC1.cmd('ip route add default via 10.10.10.4')
    PC1.cmd('ip -6 route add default via fd24:ec43:12ca:c001:10::4')

    PC4.cmd('ip -6 addr flush dev PC4-eth0')
    PC4.cmd('ip -6 addr flush dev PC4-eth1')
    PC4.cmd('ip -6 addr flush dev PC4-eth2')
    PC1.cmd('ip -6 addr flush dev PC1-eth0')
    PC2.cmd('ip -6 addr flush dev PC2-eth0')
    PC3.cmd('ip -6 addr flush dev PC3-eth0')

    PC1.cmd('ip -6 addr add fd24:ec43:12ca:c001:10::1/80 dev PC1-eth0')
    PC2.cmd('ip -6 addr add fd24:ec43:12ca:c001:20::2/80 dev PC2-eth0')
    PC3.cmd('ip -6 addr add fd24:ec43:12ca:c001:30::3/80 dev PC3-eth0')
    PC4.cmd('ip -6 addr add fd24:ec43:12ca:c001:10::4/80 dev PC4-eth0')
    PC4.cmd('ip -6 addr add fd24:ec43:12ca:c001:20::4/80 dev PC4-eth1')
    PC4.cmd('ip -6 addr add fd24:ec43:12ca:c001:30::4/80 dev PC4-eth2')

    "This is used to run commands on the hosts"

    info( '*** Starting terminals on hosts\n' )
    PC1.cmd(
  'xterm '
  '-xrm "XTerm.vt100.allowTitleOps: false" '
  '-xrm "XTerm.vt100.selectToClipboard: true" '
  '-xrm "XTerm.vt100.translations: #override '
  'Ctrl Shift <Key>C: copy-selection(CLIPBOARD)\\n'
  'Ctrl Shift <Key>V: insert-selection(CLIPBOARD)\\n'
  'Shift <Key>Insert: insert-selection(CLIPBOARD)" '
  '-T PC1 &'
)
    PC2.cmd(
    'xterm '
    '-xrm "XTerm.vt100.allowTitleOps: false" '
    '-xrm "XTerm.vt100.selectToClipboard: true" '
    '-xrm "XTerm.vt100.translations: #override '
    'Ctrl Shift <Key>C: copy-selection(CLIPBOARD)\\n'
    'Ctrl Shift <Key>V: insert-selection(CLIPBOARD)\\n'
    'Shift <Key>Insert: insert-selection(CLIPBOARD)" '
    '-T PC2 &'
)
    PC3.cmd(
    'xterm '
    '-xrm "XTerm.vt100.allowTitleOps: false" '
    '-xrm "XTerm.vt100.selectToClipboard: true" '
    '-xrm "XTerm.vt100.translations: #override '
    'Ctrl Shift <Key>C: copy-selection(CLIPBOARD)\\n'
    'Ctrl Shift <Key>V: insert-selection(CLIPBOARD)\\n'
    'Shift <Key>Insert: insert-selection(CLIPBOARD)" '
    '-T PC3 &'
)
    PC4.cmd(
    'xterm '
    '-xrm "XTerm.vt100.allowTitleOps: false" '
    '-xrm "XTerm.vt100.selectToClipboard: true" '
    '-xrm "XTerm.vt100.translations: #override '
    'Ctrl Shift <Key>C: copy-selection(CLIPBOARD)\\n'
    'Ctrl Shift <Key>V: insert-selection(CLIPBOARD)\\n'
    'Shift <Key>Insert: insert-selection(CLIPBOARD)" '
    '-T PC4 &'
)

    info( '*** Running the command line interface\n' )
    CLI( net )
	
    info( '*** Closing the terminals on the hosts\n' )
    PC1.cmd("killall xterm")
    PC2.cmd("killall xterm")
    PC3.cmd("killall xterm")
    PC4.cmd("killall xterm")
	
    info( '*** Stopping network' )
    net.stop()

"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel( 'info' )
    firstNetwork()
