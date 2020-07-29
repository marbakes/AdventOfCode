def code_to_list(codefile):
    with open(codefile, 'r') as reader:
        return [int(i) for i in reader.readlines()[0].split(",")]

def param_mode(inst, codelist, i, p):
    if (len(str(inst)) < 2 + p) or (int(str(inst)[-2 -p]) == 0):
        return codelist[codelist[i + p]]
    else:
        return codelist[i + p]

def run_opcode(codelist, inputbuffer):
    i = 0
    outputbuffer = []
    while i < len(codelist):
        inst = codelist[i]
        if len(str(inst)) < 2:
            opcode = inst
        else:
            opcode = int(str(inst)[-2:])
        if opcode == 99:
            iplus = 1
            break
        elif opcode == 1:
            iplus = 4
            try:
                codelist[codelist[i + 3]] = param_mode(inst, codelist, i, 1) + param_mode(inst, codelist, i, 2)
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        elif opcode == 2:
            iplus = 4
            try:
                codelist[codelist[i + 3]] = param_mode(inst, codelist, i, 1) * param_mode(inst, codelist, i, 2)
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        #Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. 
        #For example, the instruction 3,50 would take an input value and store it at address 50.
        elif opcode == 3:
            iplus = 2
            if len(inputbuffer) > 0:
                z = inputbuffer[0]
                inputbuffer.pop(0)
            else:
                print("Need additional input")
                break
            try:
                codelist[codelist[i + 1]] = z
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        #Opcode 4 outputs the value of its only parameter. 
        #For example, the instruction 4,50 would output the value at address 50.
        elif opcode == 4:
            iplus = 2
            try:
                z = param_mode(inst, codelist, i, 1)
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        # Opcode 5 is jump-if-true: if the first parameter is non-zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 5:
            if param_mode(inst, codelist, i, 1) != 0:
                iplus = param_mode(inst, codelist, i, 2) - i
            else:
                iplus = 3
        # Opcode 6 is jump-if-false: if the first parameter is zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 6:
            if param_mode(inst, codelist, i, 1) == 0:
                iplus = param_mode(inst, codelist, i, 2) - i
            else:
                iplus = 3
        # Opcode 7 is less than: if the first parameter is less than the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 7:
            iplus = 4
            if param_mode(inst, codelist, i, 1) < param_mode(inst, codelist, i, 2):
                s = 1
            else:
                s = 0
            codelist[codelist[i + 3]] = s
        # Opcode 8 is equals: if the first parameter is equal to the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 8:
            iplus = 4
            if param_mode(inst, codelist, i, 1) == param_mode(inst, codelist, i, 2):
                s = 1
            else:
                s = 0
            codelist[codelist[i + 3]] = s
        else:
            print(f"Error, opcode {opcode} at index {i}")
        i += iplus       
    return z

def amp_seq(input_file, phase):
    amp_in = 0
    for ph in phase:
        amp_in = run_opcode(code_to_list(input_file), [ph, amp_in])
    return amp_in

from itertools import permutations
def optimize_amp(input_file, phase_options):
    outputs = []
    for phase in permutations(phase_options):
        outputs.append(amp_seq(input_file, phase))
    return max(outputs)

# print(optimize_amp('test1.txt', (0,1,2,3,4)), 43210)
# print(optimize_amp('test2.txt', (0,1,2,3,4)), 54321)
# print(optimize_amp('test3.txt', (0,1,2,3,4)), 65210)


def run_opcode_loop(codelist, position, inputbuffer):
    i = position
    outputbuffer = []
    while i < len(codelist):
        inst = codelist[i]
        if len(str(inst)) < 2:
            opcode = inst
        else:
            opcode = int(str(inst)[-2:])
        if opcode == 99:
            iplus = 1
            return 'DONE', i, outputbuffer
        elif opcode == 1:
            iplus = 4
            try:
                codelist[codelist[i + 3]] = param_mode(inst, codelist, i, 1) + param_mode(inst, codelist, i, 2)
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        elif opcode == 2:
            iplus = 4
            try:
                codelist[codelist[i + 3]] = param_mode(inst, codelist, i, 1) * param_mode(inst, codelist, i, 2)
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        #Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. 
        #For example, the instruction 3,50 would take an input value and store it at address 50.
        elif opcode == 3:
            iplus = 2
            if len(inputbuffer) > 0:
                z = inputbuffer[0]
                inputbuffer.pop(0)
            else:
                return codelist, i, outputbuffer
            try:
                codelist[codelist[i + 1]] = z
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        #Opcode 4 outputs the value of its only parameter. 
        #For example, the instruction 4,50 would output the value at address 50.
        elif opcode == 4:
            iplus = 2
            try:
                outputbuffer.append(param_mode(inst, codelist, i, 1))
            except:
                print(f"References out of bounds after instruction {inst}")
                break
                return []
        # Opcode 5 is jump-if-true: if the first parameter is non-zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 5:
            if param_mode(inst, codelist, i, 1) != 0:
                iplus = param_mode(inst, codelist, i, 2) - i
            else:
                iplus = 3
        # Opcode 6 is jump-if-false: if the first parameter is zero, 
        # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        elif opcode == 6:
            if param_mode(inst, codelist, i, 1) == 0:
                iplus = param_mode(inst, codelist, i, 2) - i
            else:
                iplus = 3
        # Opcode 7 is less than: if the first parameter is less than the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 7:
            iplus = 4
            if param_mode(inst, codelist, i, 1) < param_mode(inst, codelist, i, 2):
                s = 1
            else:
                s = 0
            codelist[codelist[i + 3]] = s
        # Opcode 8 is equals: if the first parameter is equal to the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif opcode == 8:
            iplus = 4
            if param_mode(inst, codelist, i, 1) == param_mode(inst, codelist, i, 2):
                s = 1
            else:
                s = 0
            codelist[codelist[i + 3]] = s
        else:
            print(f"Error, opcode {opcode} at index {i}")
        i += iplus       
    return codelist, i, outputbuffer

def optimize_amp_loop(input_file, phase_options):
    outputs = []
    for phase in permutations(phase_options):
        ampA, iA, a = run_opcode_loop(code_to_list(input_file),0, [phase[0], 0])
        ampB, iB, b = run_opcode_loop(code_to_list(input_file),0, [phase[1], a[0]])
        ampC, iC, c = run_opcode_loop(code_to_list(input_file),0, [phase[2], b[0]])
        ampD, iD, d = run_opcode_loop(code_to_list(input_file),0, [phase[3], c[0]])
        ampE, iE, e = run_opcode_loop(code_to_list(input_file),0, [phase[4], d[0]])
        while ampE != 'DONE':
            ampA, iA, a = run_opcode_loop(ampA, iA, e)
            ampB, iB, b = run_opcode_loop(ampB, iB, a)
            ampC, iC, c = run_opcode_loop(ampC, iC, b)
            ampD, iD, d = run_opcode_loop(ampD, iD, c)
            ampE, iE, e = run_opcode_loop(ampE, iE, d)
        outputs.append(e[0])
    return max(outputs)
print(optimize_amp_loop('test4.txt', (5,6,7,8,9)), 139629729)
print(optimize_amp_loop('test5.txt', (5,6,7,8,9)), 18216)
print(optimize_amp_loop('input.txt', (5,6,7,8,9)))
