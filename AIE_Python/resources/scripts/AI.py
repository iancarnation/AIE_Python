# AI behaviors and movement patterns
import Level_Grid

# Defines offsets and movement costs for nodes adjacent to another node
class AdjacentNode(object):
	def __init__(self, offset, cost):
		self.offset = int(offset)
		self.cost = int(cost)

# A* Pathfinding
class AStar(object):
	def __init__(self, levelGrid):
		self.level = levelGrid
		self.nodes = levelGrid.levelTiles
		self.openList = []
		self.closedList = []
		# set of nodes adjacent to any given node (based on tile index) 
		# the cost of moving along a diagonal is 1.4 times the cost of vert. or horiz. movement
		self.AdjacentNodes = [AdjacentNode(-(levelGrid.levelWidth + 1), 14),
							  AdjacentNode(- levelGrid.levelWidth	  , 10),
							  AdjacentNode(-(levelGrid.levelWidth - 1), 14),
							  AdjacentNode(- 1 						  , 10),
							  AdjacentNode(  1 						  , 10),
							  AdjacentNode(  levelGrid.levelWidth - 1 , 14),
							  AdjacentNode(  levelGrid.levelWidth     , 10),
							  AdjacentNode(  levelGrid.levelWidth + 1 , 14)]

		self.path = []

	def Clear(self):
		self.openList = []
		self.closedList = []
		self.path = []

	def GetHeuristic(self, node):
		"""Compute the heuristic value H for a node: distance between this node and the ending node
		"""
		# ** fix this **  calculate number of x and y tiles away and multiply by 10
		return abs(self.nodes[node].x - self.nodes[self.goalNode].x) + abs(self.nodes[node].y - self.nodes[self.goalNode].y)

	def UpdateNode(self, adjIndex, adj, current):
		self.nodes[adjIndex].g = self.nodes[current].g + adj.cost
		self.nodes[adjIndex].h = self.GetHeuristic(adjIndex)
		self.nodes[adjIndex].parent = current
		self.nodes[adjIndex].f = self.nodes[adjIndex].g + self.nodes[adjIndex].h

	def PrintTileReachable(self):
		for tile in range(len(self.nodes)):
			if self.nodes[tile].isReachable():
				print "Tile %s is reachable." % (tile)

	def Run(self, startNode, goalNode):
		print "Starting Pathfinder.Run()"
		self.goalNode = goalNode
		self.startNode = startNode
		print "Start Node: %s, Goal Node: %s" % (startNode, goalNode)
		# add starting node to the open openList
		self.openList.append(startNode)
		# while open list is not empty:
		while len(self.openList) > 0:
		# - current node = node from open list with the lowest cost
			currentNode = self.FindCheapest()
			print "currentNode = %s" %(currentNode)
			if currentNode == goalNode:
		# - - path complete
				print "Path Complete!---------------------------------------------------------------------------------"
				self.MakePath()
				return self.path
			else: 
		# - - move current node to the closed list
				self.closedList.append(currentNode)
				self.openList.remove(currentNode)
		# - - search each adjacent node
				for adjNode in self.AdjacentNodes:
					adjIndex = self.nodes[currentNode + adjNode.offset].getIndex()
		# - - - if it isn't on the closed list and isn't an obstacle:
					if self.closedList.count(adjIndex) == 0 and self.nodes[adjIndex].isReachable():
		# - - - - if it is in the open list, see if current path is better than the one previously found for this adj node
						if self.openList.count(adjIndex) > 0:
							if self.nodes[adjIndex].g > self.nodes[currentNode].g + adjNode.cost:
								self.UpdateNode(adjIndex, adjNode, currentNode)
		# - - - - move it to open list and calculate cost
						else:
							self.UpdateNode(adjIndex, adjNode, currentNode)
							self.openList.append(adjIndex)

	def FindCheapest(self):
		""" Finds the node in the open list with the lowest movement cost """
		# set currentLowest to first item in list
		currentLowest = self.openList[0]
		# for each node in the open list:
		for node in self.openList:
		# - if self.nodes cost is lower than currentLowest:
			if self.nodes[node].getCost() < self.nodes[currentLowest].getCost():
		# - - set that node as currentLowest
				currentLowest = node
		return currentLowest

	def MakePath(self):
		node = self.goalNode
		self.path.append(node)
		while self.nodes[node].parent != self.startNode:
			node = self.nodes[node].parent
			self.path.insert(0,node)
			print "path: node: %s" % (self.level.resolveGridSquare(self.nodes[node].x, self.nodes[node].y))

# Dijkstra's Algorithm
class Dijkstra(object):
	def __init__(self, levelGrid):
		self.level = levelGrid
		self.nodes = levelGrid.levelTiles
		self.openList = []
		self.closedList = []
		# set of nodes adjacent to any given node (based on tile index) 
		# the cost of moving along a diagonal is 1.4 times the cost of vert. or horiz. movement
		self.AdjacentNodes = [AdjacentNode(-(levelGrid.levelWidth + 1), 14),
							  AdjacentNode(- levelGrid.levelWidth	  , 10),
							  AdjacentNode(-(levelGrid.levelWidth - 1), 14),
							  AdjacentNode(- 1 						  , 10),
							  AdjacentNode(  1 						  , 10),
							  AdjacentNode(  levelGrid.levelWidth - 1 , 14),
							  AdjacentNode(  levelGrid.levelWidth     , 10),
							  AdjacentNode(  levelGrid.levelWidth + 1 , 14)]

		self.path = []

	def Clear(self):
		self.openList = []
		self.closedList = []
		self.path = []

	def UpdateNode(self, adjIndex, adj, current):
		self.nodes[adjIndex].g = self.nodes[current].g + adj.cost
		self.nodes[adjIndex].h = 0
		self.nodes[adjIndex].parent = current
		self.nodes[adjIndex].f = self.nodes[adjIndex].g + self.nodes[adjIndex].h

	def PrintTileReachable(self):
		for tile in range(len(self.nodes)):
			if self.nodes[tile].isReachable():
				print "Tile %s is reachable." % (tile)

	def Run(self, startNode, goalNode):
		print "Starting Pathfinder.Run()"
		self.goalNode = goalNode
		self.startNode = startNode
		print "Start Node: %s, Goal Node: %s" % (startNode, goalNode)
		# add starting node to the open openList
		self.openList.append(startNode)
		# while open list is not empty:
		while len(self.openList) > 0:
		# - current node = node from open list with the lowest cost
			currentNode = self.FindCheapest()
			print "currentNode = %s" %(currentNode)
			if currentNode == goalNode:
		# - - path complete
				print "Path Complete!---------------------------------------------------------------------------------"
				self.MakePath()
				return self.path
			else: 
		# - - move current node to the closed list
				self.closedList.append(currentNode)
				self.openList.remove(currentNode)
		# - - search each adjacent node
				for adjNode in self.AdjacentNodes:
					adjIndex = self.nodes[currentNode + adjNode.offset].getIndex()
		# - - - if it isn't on the closed list and isn't an obstacle:
					if self.closedList.count(adjIndex) == 0 and self.nodes[adjIndex].isReachable():
		# - - - - if it is in the open list, see if current path is better than the one previously found for this adj node
						if self.openList.count(adjIndex) > 0:
							if self.nodes[adjIndex].g > self.nodes[currentNode].g + adjNode.cost:
								self.UpdateNode(adjIndex, adjNode, currentNode)
		# - - - - move it to open list and calculate cost
						else:
							self.UpdateNode(adjIndex, adjNode, currentNode)
							self.openList.append(adjIndex)

	def FindCheapest(self):
		""" Finds the node in the open list with the lowest movement cost """
		# set currentLowest to first item in list
		currentLowest = self.openList[0]
		# for each node in the open list:
		for node in self.openList:
		# - if self.nodes cost is lower than currentLowest:
			if self.nodes[node].getCost() < self.nodes[currentLowest].getCost():
		# - - set that node as currentLowest
				currentLowest = node
		return currentLowest

	def MakePath(self):
		node = self.goalNode
		self.path.append(node)
		while self.nodes[node].parent != self.startNode:
			node = self.nodes[node].parent
			self.path.insert(0,node)
			print "path: node: %s" % (self.level.resolveGridSquare(self.nodes[node].x, self.nodes[node].y))