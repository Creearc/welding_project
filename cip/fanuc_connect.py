from eeip import *

host = '192.168.68.103'

import time

eeipclient = EEIPClient()
#Ip-Address of the Ethernet-IP Device (In this case Allen-Bradley 1734-AENT Point I/O)
#A Session has to be registered before any communication can be established
eeipclient.register_session(host)

#Parameters from Originator -> Target
eeipclient.o_t_instance_id = 0x64
eeipclient.o_t_length = 4
eeipclient.o_t_requested_packet_rate = 100000  #Packet rate 100ms (default 500ms)
eeipclient.o_t_realtime_format = RealTimeFormat.HEADER32BIT
eeipclient.o_t_owner_redundant = False
eeipclient.o_t_variable_length = False
eeipclient.o_t_connection_type = ConnectionType.POINT_TO_POINT

#Parameters from Target -> Originator
eeipclient.t_o_instance_id = 0x65
eeipclient.t_o_length = 16
eeipclient.t_o_requested_packet_rate = 100000  #Packet rate 100ms (default 500ms)
eeipclient.t_o_realtime_format = RealTimeFormat.MODELESS
eeipclient.t_o_owner_redundant = False
eeipclient.t_o_variable_length = False
eeipclient.t_o_connection_type = ConnectionType.MULTICAST

#Forward open initiates the Implicit Messaging
eeipclient.forward_open()
while 1:
    print('State of the first Input byte: {0}'.format(eeipclient.t_o_iodata[8]))
    print('State of the second Input byte: {0}'.format(eeipclient.t_o_iodata[9]))
    time.sleep(0.1)

#Close the Session (First stop implicit Messaging then unregister the session)
eeipclient.forward_close()
eeipclient.unregister_session()














