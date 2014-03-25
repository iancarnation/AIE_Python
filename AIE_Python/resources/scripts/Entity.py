import AIE
import game

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
		
	def update(self, fDeltaTime ):
		mouseX, mouseY = AIE.GetMouseLocation()
		if( AIE.GetMouseButton(1)  ):
			self.setPositionTarget((mouseX, mouseY))
		
		if self.posTarget != self.Position:
			self.Velocity = (self.posTarget[0] - self.Position[0], self.posTarget[1] - self.Position[1])
			self.Position = (self.Position[0] + self.Velocity[0] * fDeltaTime, self.Position[1] + self.Velocity[1] * fDeltaTime)
		
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
		