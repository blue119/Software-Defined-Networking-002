'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add your logic here ...

        # code level
        core_switch = self.addSwitch('c1')

        aggr_len = 0
        edge_len = 0
        host_len = 0
        # aggregation level
        for i in xrange(fanout):
            aggr_len+=1
            ag_switch = self.addSwitch('a%d' % aggr_len)
            self.addLink(core_switch, ag_switch, **linkopts1)

            # edge level
            for j in xrange(fanout):
                edge_len+=1
                edge_switch = self.addSwitch('e%d' % edge_len)
                self.addLink(ag_switch, edge_switch, **linkopts2)

                # host
                for k in xrange(fanout):
                    host_len+=1
                    host = self.addHost('h%d' % host_len)
                    self.addLink(host, edge_switch, **linkopts3)


topos = { 'custom': ( lambda: CustomTopo() ) }

def main():
    """@todo: Docstring for main.
    :returns: @todo

    """
    linkopts1 = dict(bw=1000, delay='1ms')
    linkopts2 = dict(bw=100, delay='5ms')
    linkopts3 = dict(bw=10, delay='50ms')
    fanout = 4

    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout)
    net = Mininet(topo = topo, link=TCLink)

    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"

    h1 = net.get('h1')
    h27 = net.get('h27')

    print "Starting Test: ping h1 to h27"
    # Start pings
    outputString = h1.cmd('ping', '-c6', h27.IP())
    print outputString
    print

    #  print "Starting Test2: pingAll"
    #  net.pingAll()

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
