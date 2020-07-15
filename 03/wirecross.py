def wirecross(wirefile):
    wires = {}
    with open(wirefile, 'r') as reader:
        for i, line in enumerate(reader.readlines()):
            if i == 0:
                wire1 = []
            else:
                steps = 0
            x = 0
            y = 0
            dist = 0
            for d in line.split(","):
                try:
                    num = int(d[1:])
                except:
                    num = int(d[1:-1])
                for j in range(num):
                    if i > 0:
                        steps += 1
                    if d[0] == 'R':
                        x += 1
                    elif d[0] == 'L':
                        x -= 1
                    elif d[0] == 'U':
                        y += 1
                    elif d[0] == 'D':
                        y -= 1
                    if i == 0:
                        wire1.append((x,y))
                    else:
                        if (x,y) in wire1:
                            if (dist == 0) or (steps + wire1.index((x,y)) + 1 < dist):
                                dist = steps + wire1.index((x,y)) + 1                    
    return dist
print(f"{wirecross('test1.txt')} = 610")
print(f"{wirecross('test2.txt')} = 410")
print(wirecross('input.txt'))