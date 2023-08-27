import numpy as np
from scripts.utils import Drinker, Car, generate_arrivals


def simulate(d, v_d, dist1, dist2, v_m, v_M):
    """
    Return data containing cars and drinker trajectory.
    :param d: width of the road
    :param v_d: velocity of drinker
    :param dist1: probabilistic distribution used for generating moments of 'left cars' arrivals
    :param dist2: probabilistic distribution used for generating moments of 'right cars' arrivals
    :param v_m: minimal cars' velocity
    :param v_M: maximal cars' velocity
    """
    drinker = Drinker(v_d)
    while drinker.x < 1000:
        drinker.move()
    T = len(drinker.trajectory)
    left_arrivals = generate_arrivals(dist1, T)
    right_arrivals = generate_arrivals(dist2, T)
    cars_left = []
    cars_right = []
    cars_positions = []
    flag = True
    index = T
    for i in range(T):
        if cars_left:
            v_left_max = min([k.v for k in cars_left])
        else:
            v_left_max = v_M
        if cars_right:
            v_right_max = min([k.v for k in cars_right])
        else:
            v_right_max = v_M
        if i in left_arrivals:
            cars_left.append(Car(0, 25 + d/2, np.random.uniform(v_m, v_left_max), 1))
        if i in right_arrivals:
            cars_right.append(Car(1000, 25 - d/2, np.random.uniform(v_m, v_right_max), -1))
        cars_positions.append([k.get_position() for k in [*cars_left, *cars_right]])
        drinker_x, drinker_y = drinker.trajectory[i]
        for k in cars_left:
            if k.x - 60 <= drinker_x <= k.x and k.y - 2.5 <= drinker_y <= k.y + 2.5:
                flag = False
        for k in cars_right:
            if k.x + 60 >= drinker_x >= k.x and k.y - 2.5 <= drinker_y <= k.y + 2.5:
                flag = False
        if flag:
            for k in [*cars_left, *cars_right]:
                k.move()
        else:
            index = i + 1
            break
        cars_left = [k for k in cars_left if k.x < 1050]
        cars_right = [k for k in cars_right if k.x > -50]
    return drinker.trajectory[:index], cars_positions
