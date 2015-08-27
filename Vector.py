__author__ = 'Ken'

from math import sqrt, acos, degrees,  pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'There is no unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'There is no unique orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def dot(self, v):
        return round(sum([x*y for x, y in zip(self.coordinates, v.coordinates)]), 12)

    def times_scalar(self, v):
        new_coordinates = [Decimal(v)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def angle(self, v, in_degrees=False):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                return degrees(angle_in_radians)
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute and angle with the zero vector')
            else:
                raise e

    def normalize(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0 / magnitude))

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def is_parallel(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle(v) == 0 or
                self.angle(v) == pi)

    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else:
                raise e


# ======================================================================================== #
# ======================================================================================== #


v1 = Vector([3.039, 1.879])
b1 = Vector([0.825, 2.036])

v2 = Vector([-9.88, -3.264, -8.159])
b2 = Vector([-2.155, -9.353, -9.473])

v3 = Vector([3.009, -6.172, 3.692, -2.51])
b3 = Vector([6.404, -9.144, 2.759, 8.718])
vb = v3.component_parallel_to(b3)

print v1.component_parallel_to(b1)
print v2.component_orthogonal_to(b2)
print vb
print v3.minus(vb)
