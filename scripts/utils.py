import numpy as np


class Drinker:
    """Class implementation of a drinker."""

    def __init__(self, v):
        """Initialize class object's attributes."""
        self.x = 0
        self.y = 0
        self.v = v
        self.trajectory = [(0, 0)]

    def move(self):
        """Move drinker to a new position."""
        self.x, self.y = self.x + np.random.randn() + self.v, self.y + np.random.randn()
        self.x = abs(self.x)
        self.y = abs(self.y)
        if self.y > 50:
            self.y = 100 - self.y
        self.trajectory.append((self.x, self.y))


class Car:
    """Class implementing car object."""

    def __init__(self, x, y, v, direction):
        """Initialize class object's attributes."""
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction

    def move(self):
        """Move car to a new position."""
        self.x += self.direction * self.v

    def get_position(self):
        """Return car's position, and direction of its drive."""
        return self.x, self.y, self.direction


def mixed_poisson(Λ, T):
    """
    Return an array with moments of mixed Poisson process jumps moments.
    :param Λ: a probabilistic distribution
    :param T: time horizon
    """
    S = []
    λ = abs(Λ.rvs())
    U = np.random.rand()
    t = - 1 / λ * np.log(U)
    while t < T:
        S.append(t)
        U = np.random.rand()
        t = t - 1 / λ * np.log(U)
    return np.array(S)


def generate_arrivals(Λ, T, scale=10):
    """
    Return rounded and scaled mixed Poisson jumps moments.
    :param Λ: probabilistic distribution
    :param T: time horizon
    :param scale: scalar scaling the moments of jumps
    """
    arr = np.round(scale * mixed_poisson(Λ, T))
    return arr[arr < T]


class Unif:
    """Class implementation of a uniform distribution."""

    def __init__(self, a, b):
        """Initialize the class object's attributes."""
        self.a = a
        self.b = b

    def rvs(self):
        """Return a number from uniform U(a, b) distribution."""
        return np.random.uniform(self.a, self.b)
