def read_scanfile(scanfile):
    moons = []
    with open(scanfile, 'r') as reader:
        for line in reader.readlines():
            x = int(line[line.find('x=') + 2:line.find(',', line.find('x='))])
            y = int(line[line.find('y=') + 2:line.find(',', line.find('y='))])
            z = int(line[line.find('z=') + 2:line.find('>')])
            moons.append([x,y,z])
    return moons

def nice_number(n, digits):
    return str(int(n)).rjust(digits)

def sim_moons(scanfile, sims, interval):
    moons = read_scanfile(scanfile)
    vels = [[0,0,0] for _ in moons]

    for i in range(sims + 1):

        if i % interval == 0:
            print(f"After {i} steps:")
            for j in range(len(moons)):
                print(f"pos=<x={nice_number(moons[j][0], 3)}, y={nice_number(moons[j][1],3)}, z={nice_number(moons[j][2],3)}>, vel=<x={nice_number(vels[j][0],2)}, y={nice_number(vels[j][1],2)}, z={nice_number(vels[j][2],2)}>")
        if i == sims:
            print("")
            print(f"Energy after {sims} steps:")
            print(int(sum([sum([abs(moon[k]) for k in range(3)]) * sum([abs(vel[k]) for k in range(3)]) for moon, vel in zip(moons, vels)])))

        for j in range(len(moons)):
            for k in range(3):
                vels[j][k] += sum([(moon[k] - moons[j][k]) / abs(moon[k] - moons[j][k]) if (moon[k] != moons[j][k]) else 0 for moon in moons])

        for j in range(len(moons)):
            for k in range(3):
                moons[j][k] += vels[j][k]

sim_moons('input.txt', 1000, 1000)