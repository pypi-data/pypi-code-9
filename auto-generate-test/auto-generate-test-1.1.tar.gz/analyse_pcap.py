import socket
import sys
from testutils import dpkt_patched as dpkt
from pprint import pformat

# getting the RTCP port
from bluebox.webapi.debug.dsm_participant_list import DSMParticipant
import bluebox

def get_main_video_rtcp_port(tsip):
    ts_slave = bluebox.Box(tsip)
    participant_list = ts_slave.webapi.debug.dsm_participant_list.getpage()['participants']
    
    for participant in participant_list:
        name = participant['Endpoint']
        if any(cascade_participant in name[0] for cascade_participant in ['MASTER', 'SLAVE']):
            dsm = DSMParticipant(ts_slave, str(participant['endpointNumberRaw'])).getpage()
            transmit_address = dsm['Main video statistics']['Control']['RTCP transmit address']
            port = transmit_address.split(':')[-1].strip()
            return port

#Result Analysis in pcap
def count_mari_reports_for_cascade_link(tsmaster, tsslave):
    f = open('/root/automation/dipoza.pcap', "rb")
    pcap = dpkt.pcap.Reader(f)
    num_of_MARI_reports_sent = 0
    num_of_MARI_reports_recd = 0
    print "Main video RTCP transmit port=", get_main_video_rtcp_port(tsmaster)
    for t, buf in pcap:
      eth = dpkt.ethernet.Ethernet(buf)
      ip = eth.data # get the ip packet
      try:
        if issubclass(dpkt.udp.UDP, ip.data.__class__): # it is a udp packet
          udp = ip.data
          udp.data = dpkt.rtcp.RTCPCompound(udp.data)
          for r in udp.data:
            if (udp.dport %2 == 1): #control port
              if isinstance(r, dpkt.rtcp.RTCP_PSFB): # is it a payload specific feedback
                if r.fmt == dpkt.rtcp.RTCP_PSFB_FMT_APP_LAYER:
                  if (ip.src == tsmaster and ip.dst == tsslave):
                    num_of_MARI_reports_sent += 1
                  elif (ip.src == tsslave and ip.dst == tsmaster):
                    num_of_MARI_reports_recd += 1
      except AttributeError:
        pass
      except dpkt.dpkt.NeedData:
        pass
    OKGREEN = '\033[92m'
    print OKGREEN + "----------------------------------------------------------------"
    print OKGREEN + "Total of %d mari reports were sent from %s -> %s" % (num_of_MARI_reports_sent, tsmaster, tsslave)
    print OKGREEN + "Total of %d mari reports were recd from %s -> %s -> " % (num_of_MARI_reports_recd, tsslave, tsmaster)

    print OKGREEN + "----------------------------------------------------------------" + '\033[0m'
