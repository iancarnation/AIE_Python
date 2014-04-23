import abc

class MoveInterface(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def getVelocity(self):
		return

	@abc.abstractmethod
	def getMaxVelocity(self):
		return

	@abc.abstractmethod
	def getPosition(self):
		return

	@abc.abstractmethod
	def getMass(self):
		return