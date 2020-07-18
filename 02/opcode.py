def code_to_list(codefile):
    with open(codefile, 'r') as reader:
        return [int(i) for i in reader.readlines()[0].split(",")]

def run_opcode(codelist):
    i = 0
    while i < len(codelist):
    # for i in range(0, len(codelist), 4):
        opcode = codelist[i]
        if opcode == 99:
            p = 1
            break
        elif opcode == 2:
            p = 4
            try:
                codelist[codelist[i + 3]] = codelist[codelist[i + 1]] * codelist[codelist[i + 2]]
            except:
                print("References out of bounds")
                break
                return []
        elif opcode == 1:
            p = 4
            try:
                codelist[codelist[i + 3]] = codelist[codelist[i + 1]] + codelist[codelist[i + 2]]
            except:
                print("References out of bounds")
                break
                return []
        else:
            print(f"Error, opcode {opcode} at index {i}")
        i += p
                
    return codelist

final_code = 19690720

for n in range(100):
    for v in range(100):
        codelist = code_to_list('input.txt')
        codelist[1] = n
        codelist[2] = v
        if run_opcode(codelist)[0] == final_code:
            print(f'What is 100 * noun + verb? {100 * n + v}')
            break
        else:
            pass