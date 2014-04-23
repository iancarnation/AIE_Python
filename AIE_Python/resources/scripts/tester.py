import Utilities
import math
MAX_FORCE			= 10

a = Utilities.Vector([2,3])
b = Utilities.Vector([1,1,1])
c = b

b.truncate(0.5)

print b

b.normalize()
print b

steering = Utilities.Vector([-2.2,-1.9])

print 
