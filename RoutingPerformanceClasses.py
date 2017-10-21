class network:

	def __init__(self):
		self._links = []

	def add_link(self, link):
		if link not in self._links:
			self._links.append(link)

	def delete_link(self, link):
		self._links.remove(link)

	def __str__(self):
		string = ""
		for link in self._links:
			string += (str(link) + '\n')
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

	def __str__(self):
		string = ("%s \t %s \t %d \t %d/%d \n" \
			%(self._nodeA, self._nodeB, self._delay, len(self._connections), self._capacity))
		return string

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._nodeA in (other._nodeA+other._nodeB):
				if self._nodeB in (other._nodeA+other._nodeB):
					return True
		return False

class request:

	def __init__(self, start_time, source_node, destination_node, duration):
		self._start_t = start_time
		self._source_node = source_node
		self._dest_node = destination_node
		self._dur = duration

	def __str__(self):
		string = ("%f \t %s \t %s \t %f \n" \
			%(self._start_time, self._source_node, self._dest_node, self._dur))
		return string

class connection:

	def __init(self, source_node, destination_node, end_time):
		self._source_node = source_node
		self._dest_node = destination_node
		self._end_time = end_time

	def __str__(self):
		string = ("%s \t %s \t %f \n" \
			%(self._source_node, self._dest_node, self._end_time))
		return string




