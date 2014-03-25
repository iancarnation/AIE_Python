# AI behaviors and movement patterns
import Level_Grid

# A* Pathfinding
class AStar(object):
	def __init__(self, levelGrid):
		self.nodes = levelGrid.levelTiles
		self.open = []
		heapq.heapify(self.open)
		self.closed = set()
		
	# def __repr__(self):
	# 	return "Open: %s \n Closed: %s

	def GetHeuristic(self, node):
		"""Compute the heuristic value H for a node: distance between this node and the ending node
		"""
		return abs(node.x - self.goalNode.x) + abs(node.y - self.goalNode.y)

	def GetCell(self, x, y):
		""" Returns a node from the node list """
		return self.nodes[]

	def GetAdjacent(self, node):
		""" Returns a list of all nodes adjacent to the currentNode parameter """
		adjacents = []
		tileWidth = self.grid.tileSize['width']
		tileHeight = self.grid.tileSize['height']

		if node.x < self.grid.levelWidth - tileWidth:
			adjacents.append()

		for node in self.openList:
			# if the difference between two nodes' x and y coord. is <= tile width and height respectively, they are adjacent
			if abs(currentNode.x - node.x) <= tileWidth && abs(currentNode.y - node.y) <= tileHeight:
				adjacents.append(node)

		return adjacents

	def Run(self, startNode, goalNode):
		self.goalNode = goalNode
		self.startNode = startNode
		# add starting node to the open openList
		self.openList.append(startNode)
		# while open list is not empty:
		while len(openList) > 0:
		# - current node = node from open list with the lowest cost
			currentNode = FindCheapest()
		# - if current node = goal node:
			if currentNode == goalNode:
		# - - path complete
				break
			else: 
		# - - move current node to the closed list
				closedList.append(currentNode)
				openList.remove(currentNode)
		# - - examine each node adjacent to the current node
				adjacentNodes = GetAdjacent(currentNode)
		# - - for each adjacent node:
				for node in adjacentNodes:
		# - - - if it isn't on the open list and isn't on the closed list and isn't an obstacle:
					if openList.count(node) == 0 && closedList.count(node) == 0 && not node.bShouldDraw:
		# - - - - move it to open list and calculate cost
						openList.append(node)

	def FindCheapest(self):
		""" Finds the node in the open list with the lowest movement cost """
		# set currentLowest to first item in list
		currentLowest = self.openList[0]
		# for each node in the open list:
		for node in self.openList:
		# - if nodes cost is lower than currentLowest:
			if node.getCost() < currentLowest.getCost():
		# - - set that node as currentLowest
				currentLowest = node
		# return currentLowest
		return currentLowest