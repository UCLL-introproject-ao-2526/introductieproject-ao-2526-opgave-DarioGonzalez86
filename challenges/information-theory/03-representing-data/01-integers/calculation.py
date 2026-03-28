# How much is `10110101011` plus two?

def calculation():
    sum = int('10110101011', 2) + 2
    return bin(sum)[2:]


print(calculation())


print(int('10110101011', 2))
print(int('10110101101', 2))
