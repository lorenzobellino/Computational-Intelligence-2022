cb = [[-1, 15, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]

pb = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]


for r1, r2 in zip(pb, cb):
    for c1, c2 in zip(r1, r2):
        if c1 != c2:
            print(f"r:{cb.index(r2)} c={r2.index(c2)}")
            pm = (cb.index(r2), r2.index(c2))

move = (3 - pm[0], 3 - pm[1])
print(move)


pp = sum(sum(cb, [])) - sum(sum(pb, [])) - 1

print(pp)

import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

for r, g in enumerate(zip(a, b)):
    print(f" r:{r} g:{g}")
