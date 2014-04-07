import AIE
import game
import math

class MapLocation:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#This is just a simple Level Grid that sets up a grid based level that fills the entire screen
#this level is static in that is is the size of the viewport and no larger should you wish to create a 
#level that can be larger than the screen bounds then modify away.
#Tiles in the level can be turned off and on by a simple click of the left mouse button

class LevelGrid:
	def __init__(self, screenProperties, tileSize ):
		self.tileSize = tileSize
		self.buttonPressed = False
		self.levelWidth = math.ceil(screenProperties['width']/ tileSize['width'])
		self.levelHeight= math.ceil(screenProperties['height']/ tileSize['height'])
		self.levelSize = self.levelWidth * (self.levelHeight+1)
		print "LevelSize :", self.levelWidth, " ", self.levelHeight
		self.levelTiles = [None] * int(self.levelSize)
		
		for i in range(int(self.levelSize)):
			self.levelTiles[i] = Tile()
			self.levelTiles[i].x = self.tileSize['width'] * (i % int(self.levelWidth))
			self.levelTiles[i].y = self.tileSize['height'] * ( (int(i)/(int(self.levelWidth))))
			print "X: %s" % self.levelTiles[i].x
			print "Y: %s" % self.levelTiles[i].y
			self.levelTiles[i].index = i # store the master index of tile...may not end up using this
	
	def loadSprites(self):
		#load all sprites for each tile
		for i in range(int(self.levelSize)):
			spriteID = AIE.CreateSprite( self.levelTiles[i].getImageName(), self.tileSize['width'], self.tileSize['height'], 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0xff, 0xff, 0xff, 0xff )
			self.levelTiles[i].setSpriteID(spriteID)
			#Move Tile to appropriate location
			AIE.MoveSprite( self.levelTiles[i].getSpriteID(), self.levelTiles[i].x, self.levelTiles[i].y )
	
	def update(self, fDeltaTime):
		mouseX, mouseY = AIE.GetMouseLocation()
		
		if( AIE.GetMouseButton(0)  and (self.buttonPressed is False) ):
			self.buttonPressed = True
			tileIndex = int(self.resolveGridSquare(mouseX, mouseY))
			if( tileIndex >= 0 and tileIndex < self.levelSize ):
				self.levelTiles[tileIndex].setDraw()
				
		self.buttonPressed = not AIE.GetMouseButtonRelease(0)		
		
		
	def draw(self):
		for i in range( int(self.levelSize) ):
			if( self.levelTiles[i].shouldDraw() ):
				AIE.DrawSprite( self.levelTiles[i].getSpriteID() )
	
	def resolveGridSquare(self, xPos, yPos):
		xGridPos = math.floor(xPos/self.tileSize['width'])
		yGridPos = math.floor(yPos/self.tileSize['height'])
		return (yGridPos * self.levelWidth) + xGridPos
	
	def cleanUp(self):
		for i in range( int(self.levelSize) ):
			if( self.levelTiles[i].getSpriteID() != -1 ):
				AIE.DestroySprite( self.levelTiles[i].getSpriteID() )

#A simple tile class that is set up to control each individual tile in the game level
#each tile has a sprite ID and can be turned on or off to allow for tiles to be drawn or not.				
class Tile:
	def __init__(self):
		self.imageName = "./images/Red_Desert.jpg"
		self.spriteID = -1
		self.bShouldDraw = True
		self.state = 0
		self.x = 0
		self.y = 0

		self.reachable = self.bShouldDraw # temporarily making non-drawers also non-reachables
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0
	
	def getImageName(self):
		return self.imageName
		
	def getState(self):
		return self.state
	
	def getSpriteID(self):
		return self.spriteID

	def getIndex(self):
		return self.index
		
	def setSpriteID(self, a_spriteID):
		self.spriteID = a_spriteID
	
	def setDraw(self):
		self.bShouldDraw = not self.bShouldDraw
		#self.reachable = not self.reachable
	
	def shouldDraw(self):
		return self.bShouldDraw

	def Equals(self, a_tile):
		if self.x == a_tile.x and self.y == a_tile.y:
			return True
		else:
			return False

	# A* info ----------------------------------------------

	def getCost(self):
		self.f = self.g + self.h
		return self.f



