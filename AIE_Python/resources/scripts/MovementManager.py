# based on: http://gamedevelopment.tutsplus.com/tutorials/understanding-steering-behaviors-movement-manager--gamedev-4278

import Utilities

MAX_FORCE = 100

class MovementManager(object):
	def __init__(self, interface):
		self.host = interface
		self.steering = Utilities.Vector([0.0,0.0])

	def update(self):
		self.velocity = self.host.getVelocity()
		self.position = self.host.getPosition()

		global MAX_FORCE
		self.steering.truncate(MAX_FORCE)
		self.steering *= (1.0 / self.host.getMass())

		self.velocity += self.steering

		self.position += self.velocity

	# The publish method
	# Recieves a target to seek and a slowingRadius (used to perform arrive)
	def seek(self, target, slowingRadius = 50):
		self.steering += self._doSeek(target, slowingRadius)

	# Actual implementation of seek (with arrival code included)
	def _doSeek(self, target, slowingRadius = 0):
		force = Utilities.Vector([0.0,0.0])

		desired = target - self.host.getPosition()

		distance = desired.getMagnitude()
		
		desired.normalize()

		if (distance <= slowingRadius):
			desired *= (self.host.getMaxVelocity() * distance / slowingRadius)
		else:
			desired *= self.host.getMaxVelocity()

		force = desired - self.host.getVelocity()

		return force

	def flee(self, target):
		self.steering += self._doFlee(target)

	def _doFlee(self, target):
		force = Utilities.Vector([0.0,0.0])

		desired = self.host.getPosition() - target
		
		desired.normalize()

		desired *= self.host.getMaxVelocity()

		force = desired - self.host.getVelocity()

		return force










