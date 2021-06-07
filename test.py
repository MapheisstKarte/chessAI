import time

from numba import jit


@jit(target="cuda")
def add(x):
    for i in range(1000000):
        x += 1
        print(x)


def add2(y):
    for i in range(1000000):
        y += 1
        print(y)


x = 0
y = 0

time1 = time.time()
add(x)
print(str(time.time() - time1))
