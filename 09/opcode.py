def code_to_list(codefile):
    with open(codefile, 'r') as reader:
        return [int(i) for i in reader.readlines()[0].split(",")]

def param_mode(inst, codelist, i, p, base):
    if (len(str(inst)) < 2 + p) or (int(str(inst)[-2 -p]) == 0):
        position = codelist[i + p]
    elif int(str(inst)[-2 -p]) == 1:
        position = i + p
    elif int(str(inst)[-2 -p]) == 2:
        position = codelist[i + p] + base
    if position > len(codelist) - 1:
        codelist = pad_code(codelist, position)
    return codelist[position]

def write_mode(inst, codelist, i, p, base):
    if (len(str(inst)) < 2 + p) or (int(str(inst)[-2 -p]) == 0):
        position = codelist[i + p]
    elif int(str(inst)[-2 -p]) == 1:
        position = i + p
    elif int(str(inst)[-2 -p]) == 2:
        position = codelist[i + p] + base
    if position > len(codelist) - 1:
        codelist = pad_code(codelist, position)
    return position

def pad_code(codelist, p):
    return codelist + [0] * (p-len(codelist) + 1)

def run_opcode(codelist, z):
    i = 0
    base = 0
    while i < len(codelist):
        inst = codelist[i]
        if len(str(inst)) < 2:
            opcode = inst
        else:
            opcode = int(str(inst)[-2:])
        if opcode == 99:
            iplus = 1
            print(f"Halted at index {i} out of {len(codelist)}")
            break
        elif opcode == 1:
            iplus = 4
            try:
                codelist[write_mode(inst, codelist, i, 3, base)] = param_mode(inst, codelist, i, 1, base) + param_mode(inst, codelist, i, 2, base)
            except:
                codelist = pad_code(codelist, write_mode(inst, codelist, i, 3, base))
                codelist[write_mode(inst, codelist, i, 3, base)] = param_mode(inst, codelist, i, 1, base) + param_mode(inst, codelist, i, 2, base)             
        elif opcode == 2:
            iplus = 4
            try:
                codelist[write_mode(inst, codelist, i, 3, base)] = param_mode(inst, codelist, i, 1, base) * param_mode(inst, codelist, i, 2, base)
            except:
                codelist = pad_code(codelist, write_mode(inst, codelist, i, 3, base))
                codelist[write_mode(inst, codelist, i, 3, base)] = param_mode(inst, codelist, i, 1, base) * param_mode(inst, codelist, i, 2, base)
        #Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. 
        #For example, the instruction 3,50 would take an input value and store it at address 50.
        elif opcode == 3:
            iplus = 2
            try:
                codelist[write_mode(inst, codelist, i, 1, base)] = z
            except:
                codelist = pad_code(codelist, codelist[i + 1])
                codelist[write_mode(inst, codelist, i, 1, base)] = z
        #Opcode 4 outputs the value of its only parameter. 
        #For example, the instruction 4,50 would output the value at address 50.
        elif opcode == 4:
            iplus = 2
            try:
                z = param_mode(inst, codelist, i, 1, base)
                print(f"Output: {z} at index {i} with instruction {inst}")
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        # Opcode 5 is jump-if-true: if the first parameter is non-zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 5:
            if param_mode(inst, codelist, i, 1, base) != 0:
                iplus = param_mode(inst, codelist, i, 2, base) - i
            else:
                iplus = 3
        # Opcode 6 is jump-if-false: if the first parameter is zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 6:
            if param_mode(inst, codelist, i, 1, base) == 0:
                iplus = param_mode(inst, codelist, i, 2, base) - i
            else:
                iplus = 3
        # Opcode 7 is less than: if the first parameter is less than the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 7:
            iplus = 4
            if param_mode(inst, codelist, i, 1, base) < param_mode(inst, codelist, i, 2, base):
                s = 1
            else:
                s = 0
            try:
                codelist[write_mode(inst, codelist, i, 3, base)] = s
            except:
                codelist = pad_code(codelist, write_mode(inst, codelist, i, 3, base))
                codelist[write_mode(inst, codelist, i, 3, base)] = s
        # Opcode 8 is equals: if the first parameter is equal to the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 8:
            iplus = 4
            if param_mode(inst, codelist, i, 1, base) == param_mode(inst, codelist, i, 2, base):
                s = 1
            else:
                s = 0
            try:
                codelist[write_mode(inst, codelist, i, 3, base)] = s
            except:
                codelist = pad_code(codelist, write_mode(inst, codelist, i, 3, base))
                codelist[write_mode(inst, codelist, i, 3, base)] = s
        # Opcode 9 adjusts the relative base by the value of its only parameter. 
        # The relative base increases (or decreases, if the value is negative) by the value of the parameter.
        elif opcode == 9:
            iplus = 2
            base += param_mode(inst, codelist, i, 1, base)
        else:
            print(f"Error, opcode {opcode} at index {i}")
        i += iplus       
    return z

print(run_opcode(code_to_list('input.txt'), 2))