def fuel(m):
    return int(m)//3 - 2

def total_fuel(module):
    module_fuel = [fuel(module)]
    while module_fuel[-1] > 0:
        module_fuel.append(fuel(module_fuel[-1]))
        if module_fuel[-1] <= 0:
            module_fuel = module_fuel[:-1]
            break
    return sum(module_fuel)

with open('input.txt', 'r') as reader:
    modules_list = reader.readlines()

print(sum([total_fuel(mass) for mass in modules_list]))