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

# functions
'''
def routing_protocols(source_node, desti_node):
	new_rout = routing()
	new_rout._rout.append(source_node)
	cost_record = [source_node, 0]
	routs = [new_rout]
	done = 0
	print(routs)
	while done == 0:
		# for all backup routs
		num_of_del = 0
		for i in range(len(routs)):
			print('i is %d'%i)
			last_node = routs[i-num_of_del]._rout[len(routs[i-num_of_del]._rout)-1]
			index_fork = virtual_net.get_paths_index(last_node)
			delete_flag = 1
			for j in range(len(virtual_net._paths[index_fork]._to)):
				#print('j is %d'%j)
				# for each reachable node
				new_node = virtual_net._paths[index_fork]._to[j]
				index_link = virtual_net.get_link_index(last_node, new_node)
				extra_delay = virtual_net._links[index_link]._delay
				extra_load = virtual_net._links[index_link].get_link_load()
				extra_hop = 1
				if routing_scheme == 'SHP':
					extra_cost = extra_hop
				elif routing_scheme == 'SDP':
					extra_cost = extra_delay
				elif routing_scheme == 'LLP':
					extra_cost = extra_load
				else:
					print('wrong ROUTING_SCHEME input')
					extra_cost = 0
				new_cost = routs[i-num_of_del]._cost + extra_cost
				buff_rout = routing()
				buff_rout._rout = routs[i-num_of_del]._rout
				buff_rout._rout.append(new_node)
				buff_rout._cost = new_cost
				buff_rout._hops = routs[i-num_of_del]._hops + extra_hop
				buff_rout._delay = routs[i-num_of_del]._delay + extra_delay
				# check and update cost_record then add routs(if required)
				for k in range(int(len(cost_record)/2)):
					#print('k is :%d'%k)
					if new_node == cost_record[k*2]:
						# this destination have record
						if new_cost < cost_record[k*2+1]:
							# new record, add to routs
							cost_record[k*2+1] = new_cost
							routs.append(buff_rout)
							delete_flag = 0
				if new_node not in cost_record:
					# this destination not recorded
					cost_record.append(new_node)
					cost_record.append(new_cost)
					routs.append(buff_rout)
					delete_flag = 0
			# this rout process done
			print(routs[i-num_of_del])
			if delete_flag == 1:
				routs.remove(routs[i-num_of_del])
				num_of_del += 1
				print('deleted')
		#print(len(routs))
		if len(routs) == 1:
			if routs[0]._rout[len(routs[0]._rout)-1] == desti_node:
				done == 1
				print("finish")
				print(routs[0])
	return routs[0]
'''

def setup_network():
	with open(topology_file, 'r') as topology:

		for line in topology:
			# read a line from file
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
			newlink = link(strs[0],strs[1],nums[0],nums[1])
			# add a link according to the file
			virtual_net.add_link(newlink)
		
		else:
			print('topology file loading complete\n')

def simulate_once():
	# these are counters
	num_request = 0
	num_success = 0
	sum_hop = 0
	sum_delay = 0

	with open(workload_file, 'r') as workload:

		for line in workload:
			# read a line from file
			strs = []
			nums = []
			read_from = 0
			read_to = line.find(' ')

			while read_to > -1:
				buff_str = line[read_from:read_to]
				read_from = read_to + 1
				read_to = line.find(' ', read_to + 1)
				try:
					buff_num = float(buff_str)
					nums.append(buff_num)
				except ValueError:
					strs.append(buff_str)

			buff_str = line[read_from:len(line)-1]
			try:
				buff_num = float(buff_str)
				nums.append(buff_num)
			except ValueError:
				strs.append(buff_str)
			# make a request according to the file
			new_request = request(nums[0],strs[0],strs[1],nums[1])
			num_request += 1
			routing_protocols(strs[0], strs[1])

		else:
			print('workload file loading complete\n')



	print(num_request, num_success,	sum_hop, sum_delay)


setup_network()
simulate_once()

print(virtual_net)

output_file.close()

