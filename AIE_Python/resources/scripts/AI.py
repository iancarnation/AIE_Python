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
		self.nodes = levelGrid.levelTiles
		self.openList = []
		self.closedList = []
		#heapq.heapify(self.open)
		#self.closedList = set()
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
		
	# def __repr__(self):
	# 	return "Open: %s \n Closed: %s

	def GetHeuristic(self, node):
		"""Compute the heuristic value H for a node: distance between this node and the ending node
		"""
		# ** fix this **  calculate number of x and y tiles away and multiply by 10
		return abs(self.nodes[node].x - self.nodes[self.goalNode].x) + abs(self.nodes[node].y - self.nodes[self.goalNode].y)

	# def GetCell(self, x, y):
	# 	""" Returns a node from the node list """
	# 	return self.nodes[]

	# def GetAdjacent(self, currentNode):
	# 	""" Returns a list of all nodes adjacent to the currentNode parameter """
	# 	adjacents = []
	# 	tileWidth = self.grid.tileSize['width']
	# 	tileHeight = self.grid.tileSize['height']

	# 	if currentNode.x < self.grid.levelWidth - tileWidth:
	# 		adjacents.append(self.nodes[])

	# 	for node in self.openList:
	# 		# if the difference between two nodes' x and y coord. is <= tile width and height respectively, they are adjacent
	# 		if abs(currentNode.x - node.x) <= tileWidth && abs(currentNode.y - node.y) <= tileHeight:
	# 			adjacents.append(node)

	# 	return adjacents

	def UpdateNode(self, adjIndex, adj, current):
		self.nodes[adjIndex].g = self.nodes[current].g + adj.cost
		self.nodes[adjIndex].h = self.GetHeuristic(adjIndex)
		#print "heuristic: %s" %(self.nodes[adjIndex].h)
		self.nodes[adjIndex].parent = current
		self.nodes[adjIndex].f = self.nodes[adjIndex].g + self.nodes[adjIndex].h

	def Run(self, startNode, goalNode):
		self.goalNode = goalNode
		self.startNode = startNode
		print "Start Node: %s, Goal Node: %s" % (startNode, goalNode)
		path = []
		# add starting node to the open openList
		self.openList.append(startNode)
		# while open list is not empty:
		while len(self.openList) > 0:
		# - current node = node from open list with the lowest cost
			currentNode = self.FindCheapest()
			print "currentNode = %s" %(currentNode)
			if currentNode == goalNode:
		# - - path complete
				print "Path Complete!"
				break
			else: 
		# - - move current node to the closed list
				self.closedList.append(currentNode)
				self.openList.remove(currentNode)
				print "List Update: closed: %s, open: %s" % (self.closedList, self.openList)
		# - - search each adjacent node
				for adjNode in self.AdjacentNodes:
					print "currentNode: %s, adjNode offset: %s" %(currentNode, adjNode.offset)
					adjIndex = self.nodes[currentNode + adjNode.offset].getIndex()
		# - - - if it isn't on the closed list and isn't an obstacle:
					print "adjIndex = %s" %(adjIndex)
					if self.closedList.count(adjIndex) == 0 and self.nodes[adjIndex].reachable:
		# - - - - if it is in the open list, see if current path is better than the one previously found for this adj node
						if self.openList.count(adjIndex) > 0:
							if self.nodes[adjIndex].g > self.nodes[currentNode].g + adjNode.cost:
								self.UpdateNode(adjIndex, adjNode, currentNode)
		# - - - - move it to open list and calculate cost
						else:
							self.UpdateNode(adjIndex, adjNode, currentNode)
							self.openList.append(adjIndex)
							print "Node %s added to self.openList: %s" % (adjIndex, self.openList)


	def FindCheapest(self):
		""" Finds the node in the open list with the lowest movement cost """
		# set currentLowest to first item in list
		print "openList: %s" %(self.openList)
		currentLowest = self.openList[0]
		print "in FindCheapest(): is currentLowest an int?"
		print str(type(currentLowest) is int)
		# for each node in the open list:
		for node in self.openList:
		# - if self.nodes cost is lower than currentLowest:
			if self.nodes[node].getCost() < self.nodes[currentLowest].getCost():
		# - - set that node as currentLowest
				currentLowest = node
		# return currentLowest
		print "currentLowest: %s" % (currentLowest)
		return currentLowest