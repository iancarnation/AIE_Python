import AIE
import game
import AI

#Base Entity
#   Basic base class for game Entities

class BaseEntity:

	def __init__(self, size):
		self.Position = ( 800, 600 )
		self.Rotation = 0
		self.Velocity = (0,0)
		self.spriteName = "Undefined"
		self.size = size
		self.origin = (0.5, 0.5)
		self.spriteID = -1
		
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



#Tank Entity
#   A simple entity that can be placed on the screen with a right click, you should modify this so that the tank can be told to 
#   navigate to a point instead of instantly move.

class TankEntity(BaseEntity):

	def __init__(self):
		self.Position = ( 800, 600 )
		self.Rotation = 0
		self.Velocity = (0,0)
		self.spriteName = "./images/PlayerTanks.png"
		self.size = (57, 72 )
		self.origin = (0.5, 0.5)
		self.spriteID = AIE.CreateSprite( self.spriteName, self.size[0], self.size[1], self.origin[0], self.origin[1], 71.0/459.0, 1.0 - 72.0/158.0, 128/459.0, 1.0 , 0xff, 0xff, 0xff, 0xff )
		print "spriteID", self.spriteID
		#Move Tile to appropriate location
		
		self.turret = Turret(self)
		self.posTarget = self.Position
		self.endGoal = self.Position
		self.hasPathfinder = False
		self.pathFound = False
		self.pathFinished = False
		self.pathCount = -1
		
	def update(self, fDeltaTime, levelGrid ):
		if not self.hasPathfinder:
			self.Pathfinder = AI.AStar(levelGrid)
			self.hasPathfinder = True
		mouseX, mouseY = AIE.GetMouseLocation()
		if( AIE.GetMouseButton(1)  ):
			self.endGoal = mouseX, mouseY
		
		if self.Position != self.endGoal:
			if not self.pathFound:
				startNode = levelGrid.resolveGridSquare(self.Position[0], self.Position[1])
				targetNode = levelGrid.resolveGridSquare(self.endGoal[0], self.endGoal[1])
				print "Mouse X: %d, Mouse Y: %d" % (mouseX, mouseY)

				print "Start Node: %s, Goal Node: %s" % (startNode, targetNode)
				self.Pathfinder.Run(int(startNode), int(targetNode))
				self.pathFound = True
			if not self.pathFinished and self.Position == self.posTarget:
				self.posTarget = self.NextWaypoint(self.Pathfinder.path)
			self.Velocity = (self.posTarget[0] - self.Position[0], self.posTarget[1] - self.Position[1])
		 	self.Position = (self.Position[0] + self.Velocity[0] * fDeltaTime, self.Position[1] + self.Velocity[1] * fDeltaTime)
		else:
			self.Pathfinder.Clear()

		AIE.MoveSprite( self.spriteID, self.Position[0], self.Position[1] )
		self.turret.update(fDeltaTime)
	
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
		print "PathCount: %s / %s" % (self.pathCount, len(self.Pathfinder.path))
		if self.pathCount is not len(self.Pathfinder.path) - 1:
			self.pathCount += 1
			print 
			return game._level.resolveNodeCenter(self.Pathfinder.path[self.pathCount])
		else:
			self.pathFinished = True
			print "Path Travelled"
			self.pathCount = -1
			return game._level.resolveNodeCenter(self.Pathfinder.path[self.pathCount])
		
		
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
		