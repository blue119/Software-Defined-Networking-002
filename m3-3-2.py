from mininet.net import Mininet
from mininet.topo import LinearTopo

net = Mininet()

c0 = net.addController()
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')

net.addLink(h0, s0)
net.addLink(h1, s0)

h0.setIP('192.168.1.1', 24)
h1.setIP('192.168.1.2', 24)

net.start()
net.pingAll()
net.stop()

