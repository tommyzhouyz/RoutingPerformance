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
				self._connections.append(course)
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

	def __init(self, source_node, destination_node, end_time):
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
















