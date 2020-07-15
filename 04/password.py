def repeats(i):
    return len(str(i)) != len(set(str(i)))
def ascendish(i):
    return sum([int(str(i)[j]) <= int(str(i)[j + 1]) for j in range(len(str(i)) - 1)]) == len(str(i)) - 1
def hasdouble(i):
    for n in set(str(i)):
        if str(i).count(n) == 2:
            return True
            break
    return False
passwords = 0
for i in range(156218, 652527 + 1):
    if repeats(i) and ascendish(i):
        if hasdouble(i):
            passwords += 1
print(passwords)