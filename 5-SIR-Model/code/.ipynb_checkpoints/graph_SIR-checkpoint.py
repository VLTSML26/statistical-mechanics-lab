import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from typing import List

class GraphSIR :
	
	def __init__(self, network: nx.Graph, initial_infected: List[int], beta: float, gamma: float) -> None :
		"""
		CONSTRUCTOR:
		Initialize a SIR model on a network.
		#
		make sure node in initial_infected list are really nodes of the network
		#
		set initial status of nodes as node att
		#
		make sure params make sense 
		#
		store parameters
		#
		store info of initial condition
		"""
		#
		for node in initial_infected :
			assert node in network.nodes
		#
		nx.set_node_attributes(network, 'S', name='kind')
		for node in initial_infected :
			network.nodes[node]['kind'] = 'I'
		#
		assert (0 < beta < 1)
		assert (0 < gamma < 1)
		# 
		self.network = network
		self.beta = beta
		self.gamma = gamma
		self.history = []
		#
		self._log()
	
	def show(self, with_pos=True, ax=None, node_size=200) : #label=True
		"""
		SHOW HEX:
		Display the lattice with colored nodes depending on their attribute 'kind'.
		#
		if ax is None :
			create a fig with some features that will be returned
		#
		get positions and kinds
		#
		color the nodes
		#
		draw the network
		#
		if ax was None :
			also return ax, otherwise it is a void function
		"""
		#
		ax_was_none = ax is None
		if ax_was_none :
			fig, ax = plt.subplots(1, 1, figsize=(10, 10))
			ax.set_aspect(1)
			ax.set_axis_off()
		#
		if with_pos :
			positions = nx.get_node_attributes(self.network, 'pos')
		kinds = nx.get_node_attributes(self.network, 'kind')
		#
		node_color = []
		for node in self.network.nodes :
			if self.network.nodes[node]['kind'] == 'S' :
				node_color.append('blue')
			elif self.network.nodes[node]['kind'] == 'I' :
				node_color.append('red')
			else :
				node_color.append('green')
		#
		#nx.draw_networkx(self.network, pos=positions, node_size=node_size, node_color=node_color, ax=ax, with_labels=label)
		if with_pos :
			nx.draw(self.network, pos=positions, node_size=node_size, node_color=node_color, ax=ax)
		else :
			nx.draw(self.network, node_size=node_size, node_color=node_color, ax=ax)
		#
		if ax_was_none :
			return fig, ax
	
	def run(self, num_timesteps: int) :
		"""
		RUN:
		Run SIR dynamics for num_timsteps steps.
		"""
		for _ in range(num_timesteps) :
			self._step()
			self._log()
	
	def _step(self) :
		"""
		STEP:
		Do one discrete timestep.
		#
		for each node :
			if node is infected:
				recover with probability gamma
		#
		for each edge :
			if there is an edge S-I or I-S:
				infect the S with probability beta
		"""
		#
		for node in self.network.nodes :
			if self.network.nodes[node]['kind'] == 'I' :
				x = np.random.uniform()
				if x < self.gamma :
					self.network.nodes[node]['kind'] = 'R'
		#
		for edge in self.network.edges :
			for i in range(len(edge)) :
				if self.network.nodes[edge[i]]['kind'] == 'I' :
					if self.network.nodes[edge[(i+1)%2]]['kind'] == 'S' :
						x = np.random.uniform()
						if (x<self.beta) :
							self.network.nodes[edge[(i+1)%2]]['kind'] = 'I'
	
	def _log(self) :
		"""
		LOG:
		Store infos about actual lattice configuration.
		#
		initialize counters for S, I and R
		for each node :
			count how many nodes of the 3 kinds there are
		#
		check if the count was good: S+R+I must equal total number of nodes
		#
		add infos to the history log
		"""
		#
		varS, varI, varR = 0,0,0
		for node in self.network.nodes :
			if self.network.nodes[node]['kind'] == 'S' :
				varS += 1
			elif self.network.nodes[node]['kind'] == 'I' :
				varI += 1
			else :
				varR += 1
		#
		assert varS + varR + varI == self.network.number_of_nodes()
		#
		info = [varS, varI, varR] 
		self.history.append(info)