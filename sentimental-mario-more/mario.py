import cs50


# height is +ve
while True:
    x = cs50.get_int("height:")
    if x > 0 and x < 9:
        break
# print pyramid
for i in range(1, x + 1):
    for j in range(x, i, -1):
        print(' ', end='')
    for j in range(i):
        print('#', end='')
    print('  ', end='')
    for j in range(x, i):
        print(' ', end='')
    for j in range(i):
        print('#', end='')
    print()