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
def routing_protocols(source_node, desti_node):
	cost_record = [source_node, 0]
	backup_routs = routing_set()
	new_rout = routing()
	new_rout._rout.append(source_node)
	backup_routs.add_rout(new_rout)
	done = 0
	# print(backup_routs)
	while done == 0:
		# for all backup routs
		print(backup_routs)
		num_of_routs = len(backup_routs._all_routs)
		for i in range(num_of_routs):
			#print('i is %d'%i)
			#print(len(backup_routs._all_routs))
			#print(num_of_routs)
			#print(num_of_del)
			# from back to front
			dealing_index = num_of_routs-1-i
			current_rout_info = backup_routs._all_routs[dealing_index]
			last_node = current_rout_info._rout[len(current_rout_info._rout)-1]
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
				#print(current_rout_info)
				new_cost = current_rout_info._cost + extra_cost
				#buff_rout = routs[i]
				buff_rout = routing()

				buff_rout.copy_routing(current_rout_info)

				buff_rout._rout.append(new_node)
				buff_rout._cost = new_cost
				buff_rout._hops += extra_hop
				buff_rout._delay += extra_delay
				#print(buff_rout)
				#print(current_rout_info)
				#print('\n')
				# check and update cost_record then add routs(if required)
				for k in range(int(len(cost_record)/2)):
					#print('k is :%d'%k)
					if new_node == cost_record[k*2]:
						# this destination have record
						if new_cost < cost_record[k*2+1]:
							# new record, add to routs
							cost_record[k*2+1] = new_cost
							backup_routs.add_rout(buff_rout)
							delete_flag = 0
				if new_node not in cost_record:
					# this destination not recorded
					cost_record.append(new_node)
					cost_record.append(new_cost)
					backup_routs.add_rout(buff_rout)
					delete_flag = 0
			# this rout process done
			if delete_flag == 1:
				if current_rout_info.get_last_node() != desti_node:
					#print(current_rout_info)
					#print(current_rout_info.get_last_node())
					#print(desti_node)
					backup_routs.delete_rout(current_rout_info)
					#print('deleted, %d left'%len(backup_routs._all_routs))
		#print(len(routs))
		if len(backup_routs._all_routs) == 1:
			left_rout = backup_routs._all_routs[0]
			#print(left_rout)
			if left_rout.get_last_node() == desti_node:
				done = 1
				print("finish")
				#print(done)
	print(left_rout)
	return backup_routs._all_routs[0]

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

