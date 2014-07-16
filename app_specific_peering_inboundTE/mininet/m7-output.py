
'''
Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

import os, time
from sdx_mininext import *


def output():
	"""Uses the student code to compute the output for test cases."""
	outputString = ''

	f = open('output.log', 'w')
	topo = QuaggaTopo()
	net = Mininext(topo=topo,
		controller=lambda name: RemoteController( name, ip='127.0.0.1' ),listenPort=6633)

	net.start()
	addInterfacesForSDXNetwork(net)
	
	a1 = net.get('a1')
    	b1 = net.get('b1')
    	c1 = net.get('c1')
    	c2 = net.get('c2')
	while True:
		routingDump = a1.cmdPrint('route -n')
        	n_routes = len(routingDump.split('a1-eth0'))-1
		# Make sure that your routing table has 7 entries
		if n_routes ==7:
			outputString += routingDump
			break
		else:
			time.sleep(2)
	b1.cmdPrint('iperf -s -B 140.0.0.1 -p 80 &')
	c2.cmdPrint('iperf -s -B 180.0.0.1 -p 80 &')
	outputString += a1.cmd('iperf -c 140.0.0.1 -B 100.0.0.1 -p 80 -t 2')
	outputString += a1.cmd('iperf -c 180.0.0.1 -B 100.0.0.2 -p 80 -t 2')
	net.stop()
	print "---Test Completed---"
	#print outputString
	f.write(outputString)
	f.close()

output()
