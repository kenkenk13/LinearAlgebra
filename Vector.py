__author__ = 'Ken'

from math import sqrt, acos, degrees,  pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

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
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])

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


v1 = Vector([-7.579, -7.88])
v2 = Vector([-2.029, 9.97, 4.172])
v3 = Vector([-2.328, -7.284, -1.214])
v4 = Vector([2.118, 4.827])

w1 = Vector([22.737, 23.64])
w2 = Vector([-9.231, -6.639, -7.245])
w3 = Vector([-1.821, 1.072, -2.94])
w4 = Vector([0, 0])

# print v1.is_parallel(w1)
print v1.is_orthogonal(w1)
print v2.is_parallel(w2)
print v2.is_orthogonal(w2)
print v3.is_parallel(w3)
print v3.is_orthogonal(w3)
print v4.is_parallel(w4)
print v4.is_orthogonal(w4)