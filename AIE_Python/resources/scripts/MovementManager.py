# based on: http://gamedevelopment.tutsplus.com/tutorials/understanding-steering-behaviors-movement-manager--gamedev-4278

import Utilities

MAX_FORCE			= 100

class MovementManager(object):
	def __init__(self, interface):
		self.host = interface
		self.steering = Utilities.Vector([0.0,0.0])

	def update(self):
		self.velocity = self.host.getVelocity()
		#print "Host Velocity Recieved: %s" % (self.velocity)
		self.position = self.host.getPosition()
		#print "Host Position Recieved: %s" % (self.position)

		global MAX_FORCE
		self.steering.truncate(MAX_FORCE)
		#print "steering after truncate: %s" % (self.steering)
		self.steering *= (1.0 / self.host.getMass())
		#print "mass: %s" % (self.host.getMass())
		#print "steering after mass: %s" % (self.steering)

		self.velocity += self.steering
		#print "update velocity: %s" % (self.velocity)

		self.position += self.velocity
		#print "update position: %s" % (self.position)

	# The publish method
	# Recieves a target to seek and a slowingRadius (used to perform arrive)
	def seek(self, target, slowingRadius = 50):
		self.steering += self._doSeek(target, slowingRadius)

	# Actual implementation of seek (with arrival code included)
	def _doSeek(self, target, slowingRadius = 0):
		force = Utilities.Vector([0.0,0.0])

		desired = target - self.host.getPosition()
		#print "desired: %s" % (desired)
		#print "target: %s minus host position: %s" % (target, self.host.getPosition())

		distance = desired.getMagnitude()
		#print "distance: %s" % (distance)
		desired.normalize()
		#print "desired: %s" % (desired)

		if (distance <= slowingRadius):
			desired *= (self.host.getMaxVelocity() * distance / slowingRadius)
		else:
			desired *= self.host.getMaxVelocity()

		force = desired - self.host.getVelocity()

		return force











