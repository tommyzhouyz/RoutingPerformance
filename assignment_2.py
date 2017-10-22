import sys
#import os

network_scheme = str(sys.argv[1])	# "CIRCUIT" OR "PACKET"
routing_scheme = str(sys.argv[2])	# "SHP", "SDP" OR "LLP"
topology_file = str(sys.argv[3])	# name of topology file
workload_file = str(sys.argv[4])	# name of workload file
packet_rate = int(sys.argv[5])		# positive integer FOR packets per sec

# open files
#output_file = open('output.txt', 'a')
#os.remove('output.txt')
output_file = open('output.txt', 'a')

# all classed used are here
class network:

	def __init__(self):
		self._links = []	# list of link
		self._paths = []	# list of fork_nodes

	def add_link(self, link):
		if link not in self._links:
			self._links.append(link)
			# update forks set (_paths), 2 nodes should be added into some fork
			nodeA_pushed = 0
			nodeB_pushed = 0
			# search for all forks in paths
			for index in range(len(self._paths)):
				if self._paths[index]._from == link._nodeA:
					# fork from node A already made in this fork, write node B in
					self._paths[index]._to.append(link._nodeB)
					nodeB_pushed = 1
				if self._paths[index]._from == link._nodeB:
					# fork from node B already made in this fork, write node A in
					self._paths[index]._to.append(link._nodeA)
					nodeA_pushed = 1
			if nodeB_pushed == 0:
				# fork from node A is not exist, creat one and write node B in
				new_fork = fork_nodes(link._nodeA)
				new_fork._to.append(link._nodeB)
				self._paths.append(new_fork)
				nodeB_pushed = 1
			if nodeA_pushed == 0:
				# fork from node B is not exist, creat one and write node A in
				new_fork = fork_nodes(link._nodeB)
				new_fork._to.append(link._nodeA)
				self._paths.append(new_fork)
				nodeA_pushed = 1

	def delete_link(self, link):
		self._links.remove(link)

	def get_paths_index(self, start_node):
		for index in range(len(self._paths)):
			if self._paths[index]._from == start_node:
				return index

	def get_link_index(self, nodeA, nodeB):
		for index in range(len(self._links)):
			if self._links[index]._nodeA == nodeA:
				if self._links[index]._nodeB == nodeB:
					return index
			if nodeB == self._links[index]._nodeA:
				if nodeA == self._links[index]._nodeB:
					return index
	def __str__(self):
		string = ""
		string += "links:\n"
		for link in self._links:
			string += (str(link) + '\n')
		string += "nodes:\n"
		for fork in self._paths:
			string += (str(fork) + '\n')
		return string

class link:

	def __init__(self, nodeA, nodeB, delay, capacity):
		self._nodeA = nodeA
		self._nodeB = nodeB
		self._delay = delay
		self._capacity = capacity
		self._connections = []

	def add_connection(self, connection):
		busy = len(self._connections)
		if busy < self._capacity:
			if connection not in self._connections:
				self._connections.append(connection)
		else:
			print('Error: link has out of capacity')

	def remove_connection(self, connection):
		self._connections.remove(connection)

	def update_link(self, time):
		# remove finished connections
		for connection in self._connections:
			if time >= connection._end_time:
				self._connections.remove(connection)

	def get_link_load(self):
		return len(self._connections)/self._capacity

	def __str__(self):
		string = ("%s\t%s\t%d\t%d/%d" \
			%(self._nodeA, self._nodeB, self._delay, len(self._connections), self._capacity))
		return string

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._nodeA in (other._nodeA+other._nodeB):
				if self._nodeB in (other._nodeA+other._nodeB):
					return True
		return False

class fork_nodes:
	# all branchs from a node
	def __init__(self, source_node):
		self._from = source_node
		self._to = []

	def add_branch(destination_node):
		if destination_node not in self._to:
			self._to.append(destination_node)

	def __str__(self):
		string = "From: %s to: "%self._from
		for nodes in self._to:
			string += nodes
		return string

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._from == other._from:
				return True
		return False

class request:

	def __init__(self, start_time, source_node, destination_node, duration):
		self._start_t = start_time
		self._source_node = source_node
		self._dest_node = destination_node
		self._dur = duration

	def __str__(self):
		string = ("%f\t%s\t%s\t%f\n" \
			%(self._start_t, self._source_node, self._dest_node, self._dur))
		return string

class connection:

	def __init__(self, source_node, destination_node, end_time):
		self._source_node = source_node
		self._dest_node = destination_node
		self._end_time = end_time

	def __str__(self):
		string = ("%s\t%s\t%f\n" \
			%(self._source_node, self._dest_node, self._end_time))
		return string

class routing:

	def __init__(self):
		self._rout = []
		self._cost = 0
		self._hops = 0
		self._delay = 0

	def copy_routing(self, other):
		if isinstance(other, self.__class__):
			self._rout = []
			for i in range(len(other._rout)):
				self._rout.append(other._rout[i])
			self._cost = other._cost
			self._hops = other._hops
			self._delay = other._delay

	def get_last_node(self):
		return self._rout[len(self._rout)-1]			

	def __str__(self):
		string = ''
		for i in range(len(self._rout)):
			string += str(self._rout[i])
		string += ('\ncost is : %f | num of hops is : %d | delay is : %f'\
				%(self._cost, self._hops, self._delay))
		return string

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._rout == other._rout:
				return True
		return False

class routing_set:

	def __init__(self):
		self._all_routs = []

	def add_rout(self, rout):
		if rout not in self._all_routs:
			self._all_routs.append(rout)

	def delete_rout(self, rout):
		self._all_routs.remove(rout)

	def __str__(self):
		string = ''
		for rout in self._all_routs:
			string += str(rout) + '\n'

		return string

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
	lowest_cost = 10000
	while done == 0:
		# for all backup routs
		num_of_routs = len(backup_routs._all_routs)
		for i in range(num_of_routs):
			# from back to front
			dealing_index = num_of_routs-1-i
			current_rout_info = backup_routs._all_routs[dealing_index]
			last_node = current_rout_info._rout[len(current_rout_info._rout)-1]
			index_fork = virtual_net.get_paths_index(last_node)
			delete_flag = 1
			for j in range(len(virtual_net._paths[index_fork]._to)):
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
				new_cost = current_rout_info._cost + extra_cost
				buff_rout = routing()

				buff_rout.copy_routing(current_rout_info)

				buff_rout._rout.append(new_node)
				buff_rout._cost = new_cost
				buff_rout._hops += extra_hop
				buff_rout._delay += extra_delay
				# check and update cost_record then add routs(if required)
				for k in range(int(len(cost_record)/2)):
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
				if current_rout_info.get_last_node() == desti_node:
					if lowest_cost >= current_rout_info._cost:
						lowest_cost = current_rout_info._cost
						delete_flag = 0
			
			if delete_flag == 1:
				backup_routs.delete_rout(current_rout_info)
		if len(backup_routs._all_routs) == 1:
			left_rout = backup_routs._all_routs[0]
			if left_rout.get_last_node() == desti_node:
				done = 1
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
			selected_routing = routing_protocols(strs[0], strs[1])
			# check if routing available
			good_routing = 1
			for i in range(selected_routing._hops):
				node_a = selected_routing._rout[i]
				node_b = selected_routing._rout[i+1]
				link_index = virtual_net.get_link_index(node_a, node_b)
				curr_link = virtual_net._links[link_index]
				curr_link.update_link(nums[0])
				if curr_link.get_link_load() == 1:
					good_routing = 0
			# make_connection
			if good_routing == 1:
				num_success += 1
				sum_delay += selected_routing._delay
				sum_hop += selected_routing._hops
				for i in range(selected_routing._hops):
					node_a = selected_routing._rout[i]
					node_b = selected_routing._rout[i+1]
					link_index = virtual_net.get_link_index(node_a, node_b)
					curr_link = virtual_net._links[link_index]
					new_connection = connection(node_a, node_b, nums[0]+nums[1])
					curr_link.add_connection(new_connection)

		else:
			# print('workload file loading complete\n')
			output_string = (routing_scheme)
			output_string += ('\ntotal number of virtual circuit requests: %d\n\
number of successfully routed requests: %d\n\
percentage of routed request: %f\n\
number of blocked requests: %d\n\
percentage of blocked request: %f\n\
average number of hops per circuit: %f\n\
average cumulative propagation delay per circuit: %f\n\n' \
				%( num_request, num_success, num_success/num_request*100, \
				num_request-num_success, (num_request-num_success)/num_request*100, \
				sum_hop/num_success, sum_delay/num_success))

			print(output_string)
			output_file.write(output_string)

setup_network()
simulate_once()

output_file.close()















