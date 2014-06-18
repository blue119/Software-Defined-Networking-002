'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''
FirewallPolicy = {}
with open(policyFile, 'r') as f:
    for l in f.readlines()[1:]:
        fields = l.replace('\n', '').split(',')
        FirewallPolicy[fields[1]] = fields[2]

class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
        for s, d in FirewallPolicy.items():
            log.debug("Setup Drop Rule (%s,%s)" % (s, d))

            msg = of.ofp_flow_mod()
            msg.match.dl_src = EthAddr(s)
            msg.match.dl_dst = EthAddr(d)
            event.connection.send(msg)

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
