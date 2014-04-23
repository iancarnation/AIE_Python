import AIE
import game
import AI
import Utilities
import abc
import MovementManager
from IBoid import MoveInterface

#Base Entity
#   Basic base class for game Entities
class BaseEntity(MoveInterface):

	def __init__(self, size):
		self.Position = Utilities.Vector([800,600])
		self.Rotation = 0
		self.Velocity = Utilities.Vector([0,0])
		self.Mass = 5
		self.Steering = MovementManager.MovementManager(self)
		self.spriteName = "Undefined"
		self.size = size
		self.origin = (0.5, 0.5)
		self.spriteID = -1

		self.posTarget = self.Position
		self.endGoal = self.Position
		self.hasPathfinder = False
		self.pathFound = False
		self.pathFinished = False
		self.pathCount = -1
		
	def update(self, fDeltaTime ):	
		AIE.MoveSprite( self.spriteID, self.Position[0], self.Position[1] )
	
	def draw(self):
		AIE.DrawSprite( self.spriteID )
		
	def getImageName(self):
		return self.imageName
		
	def getState(self):
		return self.state
	
	def getSpriteID(self):
		return self.spriteID
		
	def setSpriteID(self, a_spriteID):
		self.spriteID = a_spriteID
	
	def getPosition(self):
		return self.Position

	def cleanUp(self):
		AIE.DestroySprite( self.spriteID )
		
	def setPositionTarget(self, target):
		self.posTarget = target

	def isClose(self, target):
		return abs(self.Position[0] - target[0]) < 40 and abs(self.Position[1] - target[1]) < 40

	def Equals(self, other):
		#print "Comparing position " + str(self.Position) + " and endGoal " + str(other)
		return abs(self.Position[0] - other[0]) <= 0.05 and abs(self.Position[1] - other[1]) <= 0.05

	# IBoid methods
	def getVelocity(self):
		return self.Velocity
	def getMaxVelocity(self):
		return 3
	def getPosition(self):
		return self.Position
	def getMass(self):
		return self.Mass


#Tank Entity
#   A simple entity that can be placed on the screen with a right click, you should modify this so that the tank can be told to 
#   navigate to a point instead of instantly move.

class TankEntity(BaseEntity):

	def __init__(self):
		self.Position = Utilities.Vector([800,600])
		self.Rotation = 0
		self.Velocity = Utilities.Vector([0,0])
		self.Mass = 5
		self.Steering = MovementManager.MovementManager(self)
		self.spriteName = "./images/PlayerTanks.png"
		self.size = (57, 72 )
		self.origin = (0.5, 0.5)
		self.spriteID = AIE.CreateSprite( self.spriteName, self.size[0], self.size[1], self.origin[0], self.origin[1], 71.0/459.0, 1.0 - 72.0/158.0, 128/459.0, 1.0 , 0xff, 0xff, 0xff, 0xff )
		#print "spriteID", self.spriteID
		
		self.turret = Turret(self)
		self.posTarget = self.Position
		self.endGoal = self.Position
		self.algoChoice = "AStar"
		self.hasPathfinder = False
		self.pathFound = False
		self.pathFinished = False
		self.pathCount = -1
		
	def update(self, fDeltaTime, levelGrid ):
		if not self.hasPathfinder:
			if self.algoChoice == "Dijkstra":
				self.Pathfinder = AI.Dijkstra(levelGrid)
			elif self.algoChoice == "AStar":
				self.Pathfinder = AI.AStar(levelGrid)
			self.hasPathfinder = True

		mouseX, mouseY = AIE.GetMouseLocation()
		if( AIE.GetMouseButton(1)  ):
			self.endGoal = mouseX, mouseY
			print "Reset Pathing"
			self.ResetPathing()
			print "endGoal set at: (%s,%s)" % (mouseX, mouseY)
		# if current position is not the end goal:
		if not self.Equals(self.endGoal):
			# if a path has not yet been established:
			if not self.pathFound:
				# resolve tile index for starting location and target location
				startNode = levelGrid.resolveGridSquare(self.Position[0], self.Position[1])
				targetNode = levelGrid.resolveGridSquare(self.endGoal[0], self.endGoal[1])
				print "Start Node: %s, Target Node: %s" % (startNode, targetNode)
				# run the pathfinding algorithm
				self.path = self.Pathfinder.Run(int(startNode), int(targetNode))
				self.pathFound = True
				print "Path: " + str(self.path)
			# if not at the end of the path and close enough to the next node in the path:
			if not self.pathFinished and self.isClose(self.posTarget):
				# set a new position target to the next node in the path
				self.posTarget = self.NextWaypoint(self.Pathfinder.path)

			# apply desired steering behaviors:

		 	mouseX, mouseY = AIE.GetMouseLocation()
		 	if( AIE.GetMouseButton(0) and AIE.IsKeyDown(70) ): # L Mouse and "F"
					fleePoint = Utilities.Vector([mouseX, mouseY])
					self.Steering.flee(fleePoint)			
			else:
				self.Steering.seek(Utilities.Vector(self.posTarget))
			
		 	self.Steering.update()
		 	#print "Entity Position: %s   Steering Position: %s" % (self.Position, self.Steering.position)
		 	self.Position = self.Steering.position

		AIE.MoveSprite( self.spriteID, self.Position[0], self.Position[1] )
		self.turret.update(fDeltaTime)

		# toggle between Astar and Dijkstra
		if (AIE.IsKeyDown(80)): # "P"
			print "p pressed"
			if self.algoChoice == "AStar":
				self.algoChoice = "Dijkstra"
			elif self.algoChoice == "Dijkstra":
				self.algoChoice = "AStar"
			print self.algoChoice

	def draw(self):
		AIE.DrawSprite( self.spriteID )
		self.turret.draw()
		
	def getImageName(self):
		return self.imageName
		
	def getState(self):
		return self.state
	
	def getSpriteID(self):
		return self.spriteID
		
	def setSpriteID(self, a_spriteID):
		self.spriteID = a_spriteID
	
	def getPosition(self):
		return self.Position

	def cleanUp(self):
		self.turret.cleanUp()
		AIE.DestroySprite( self.spriteID )
		
	def setPositionTarget(self, target):
		self.posTarget = target

	def NextWaypoint(self, path):
		#print "PathCount: %s / %s" % (self.pathCount, len(path))
		if self.pathCount != len(path) - 1:
			self.pathCount += 1
			print "Next Waypoint Center Coordinates: " + str(game._level.resolveNodeCenter(path[self.pathCount]))
			return list(game._level.resolveNodeCenter(path[self.pathCount]))
		else:
			print "Path Travelled"
			self.pathFinished = True
			self.pathCount = -1
			#return game._level.resolveNodeCenter(path[self.pathCount])
			return list(self.endGoal)

	def ResetPathing(self):
		self.Pathfinder.Clear()
		self.pathFound = False
		self.pathFinished = False
		self.pathCount = -1

	# IBoid methods
	def getVelocity(self):
		return self.Velocity
	def getMaxVelocity(self):
		return 10
	def getPosition(self):
		return self.Position
	def getMass(self):
		return self.Mass


		
#Turret
#    This is an Entity Object that has an owner, it is up to you to implement inheritance (BaseEntity->Turret) 
#    The Turret's position is based on the location of it's owner, if it's owner (in this scenario a Tank) is moveable
#    The turret will move with it's base/owner

class Turret(BaseEntity):
	
	def __init__(self, owner):
		self.owner = owner
		self.Position = ( 0, 0 )
		self.Rotation = 0
		self.spriteName = "./images/PlayerTanks.png"
		self.size = (29, 60 )
		self.origin = (0.55, 0.75)
		self.spriteID = AIE.CreateSprite( self.spriteName, self.size[0], self.size[1], self.origin[0], self.origin[1], 129.0/459.0, 1.0 - 61.0/158.0, 157.0/459.0, 1.0 , 0xff, 0xff, 0xff, 0xff )
		print "spriteID", self.spriteID
	
	def update(self, fDeltaTime):
		turretLocation = self.owner.getPosition()
		AIE.MoveSprite( self.spriteID, turretLocation[0], turretLocation[1] )
		
	def draw(self):
		AIE.DrawSprite( self.spriteID )
	
	def	cleanUp(self):
		AIE.DestroySprite( self.spriteID )

	# make a control scheme
		