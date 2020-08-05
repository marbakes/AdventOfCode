def asteroid_list(asteroid_map):
    asteroids = []
    with open(asteroid_map, 'r') as reader:
        for i, row in enumerate(reader.readlines()):
            for j, column in enumerate(row):
                if column == "#":
                    asteroids.append((j,i))
    return asteroids

def asteroid_base(asteroid_map):
    asteroids =  asteroid_list(asteroid_map)
    max_reach = 0
    base = ()
    for asteroid in asteroids:
        others = [_ for _ in asteroids]
        others.remove(asteroid)
        directions = []
        for other in others:
            if other[0] == asteroid[0]:
                if other[1] > asteroid[1]:
                    directions.append('S')
                else:
                    directions.append('N')
            elif other[1] == asteroid[1]:
                if other[0] > asteroid[0]:
                    directions.append('E')
                else:
                    directions.append('W')
            else:
                if other[0] < asteroid[0]:
                    prefix = 'L'
                else:
                    prefix = 'R'
                directions.append(prefix + str((other[1] - asteroid[1]) / (other[0] - asteroid[0])))
        reach = len(set(directions))
        if reach > max_reach:
            max_reach = reach
            base = asteroid
    return max_reach, base

from math import atan2, pi
def angle(a, b):
    angle = atan2(
        b[0] - a[0],
        b[1] - a[1]
    ) * 180 / pi
    return angle

def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def sort_by_angle(e):
    return e['angle']

def sort_by_distance(e):
    return e['distance']

def vaporize_order(asteroid_map):

    base = asteroid_base(asteroid_map)[1]

    others = [{
            'location': other,
            'angle': angle(base, other),
            'distance': distance(base, other)
        } if other != base else {} for other in asteroid_list(asteroid_map)]
    others.remove({})

    others.sort(key = sort_by_distance)
    others.sort(key = sort_by_angle, reverse = True)

    a0 = others[0]['angle']
    for other in others[1:]:
        if other['angle'] == a0:
            others.remove(other)
            others.append(other)
        else:
            a0 = other['angle']
    return [other['location'] for other in others]

print(vaporize_order('input.txt')[199])
