'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()

h1_src = "00:00:00:00:00:01"
h2_src = "00:00:00:00:00:02"
h3_src = "00:00:00:00:00:03"
h4_src = "00:00:00:00:00:04"

class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")


    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):

        def _setup_flow(iport, oport):
            msg = of.ofp_flow_mod()
            msg.match.in_port = iport
            msg.actions.append(of.ofp_action_output(port = oport))
            event.connection.send(msg)

        def _setup_session(s, t):
            _setup_flow(s, t)
            _setup_flow(t, s)

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("------------ Switch %s has come up.", dpid)

        """ Add your logic here """
        # Upper Slide
        # h1 <-s1-s2-s4-> h3
        if event.dpid == 1:
            _setup_session(1, 3)
            _setup_session(2, 4)

        if event.dpid == 2:
            _setup_session(1, 2)

        if event.dpid == 3:
            _setup_session(1, 2)

        if event.dpid == 4:
            _setup_session(1, 3)
            _setup_session(2, 4)

        log.debug("------------ Setup Rules for %s done.", dpid)

        # Lower Slide
        # h2 <-s1-s3-s4-> h4




def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
