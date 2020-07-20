def orbit_list(codefile):
    with open(codefile, 'r') as reader:
        return [i.strip().split(")") for i in reader.readlines()]

def count_orbits(orbits):
    count = 0
    for p in set([i[1] for i in orbits]):
        for o in orbits:
            if o[1] == p:
                inner = o[0]
                outer = o[1]
                count += 1
                while inner != 'COM':
                    for o in orbits:
                        if o[1] == inner:
                            inner = o[0]
                            outer = o[1]
                            count += 1
    return count

print(count_orbits(orbit_list('test1.txt')))
print(count_orbits(orbit_list('input.txt')))

def lineage(orbits, p):
    lineage = []
    for o in orbits:
        if o[1] == p:
            inner = o[0]
            lineage.append(inner)
            outer = o[1]
            while inner != 'COM':
                for o in orbits:
                    if o[1] == inner:
                        inner = o[0]
                        lineage.append(inner)
                        outer = o[1]
    return lineage

def dist_between(orbits, p1, p2):
    l1, l2 = lineage(orbits, p1), lineage(orbits, p2)
    for i, p in enumerate(l1):
        if p in l2:
            return i + l2.index(p)


print(dist_between(orbit_list('test2.txt'), 'YOU', 'SAN'))
print(dist_between(orbit_list('input.txt'), 'YOU', 'SAN'))