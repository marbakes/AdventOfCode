#Fuel required to launch a given module is based on its mass. 
#Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
def fuelcounterupper(modules):
    with open(modules, 'r') as reader:
        modules_list = reader.readlines()
    total_fuel = 0
    for m in modules_list:
        total_fuel += int(m) // 3 - 2
    return total_fuel

print(fuelcounterupper('input.txt'))