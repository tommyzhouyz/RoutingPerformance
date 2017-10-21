import sys
import os
from RoutingPerformanceClasses import*

network_scheme = str(sys.argv[1])	# "CIRCUIT" OR "PACKET"
routing_scheme = str(sys.argv[2])	# "SHP", "SDP" OR "LLP"
topology_file = str(sys.argv[3])	# name of topology file
workload_file = str(sys.argv[4])	# name of workload file
packet_rate = int(sys.argv[5])		# positive integer FOR packets per sec

# open files
output_file = open('output.txt', 'a')
os.remove('output.txt')
output_file = open('output.txt', 'a')

# set up network
virtual_net = network()

with open(topology_file, 'r') as topology:
	for line in topology:
		strs = []
		nums = []
		read_from = 0
		read_to = line.find(' ')
		while read_to > -1:
			buff_str = line[read_from:read_to]
			read_from = read_to + 1
			read_to = line.find(' ', read_to + 1)
			if buff_str.isdecimal():
				nums.append(int(buff_str))
			else:
				strs.append(buff_str)
		buff_str = line[read_from:len(line)-1]
		nums.append(int(buff_str))
		# print(nums,strs)
		# print('end one line\n')
		newlink = link(strs[0],strs[1],nums[0],nums[1])
		virtual_net.add_link(newlink)
	else:
		print('topology file load complete\n')

with open(workload_file, 'r') as workload:
	for line in workload:

print(virtual_net)



