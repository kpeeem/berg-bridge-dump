# 2016.01.27 00:42:52 MSK
import linux_hub
linux_hub.set_eth_speed(10)
(eth_speed, eth_duplex, eth_auto, eth_up,) = linux_hub.get_eth_speed()
if eth_duplex:
    print 'Ethernet speed set to %dBase-T full-duplex' % eth_speed
else:
    print 'Ethernet speed set to %dBase-T half-duplex' % eth_speed

+++ okay decompyling ./set_ethernet_speed.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:52 MSK
