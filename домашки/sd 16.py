import math
import random
import sys
import numpy as np

N = 10**5
random.seed(42)  # воспроизводимый пример

values = [random.random() for _ in range(N)]

# 1. Суммирование циклом
total_loop = 0.0
for value in values:
    total_loop += value
mean_loop = total_loop / N

# 2. Встроенная sum
mean_sum = sum(values) / N

# 3. Точное суммирование с компенсацией ошибок
mean_fsum = math.fsum(values) / N

# 4. NumPy
mean_numpy = float(np.mean(values))

epsilon = sys.float_info.epsilon  # обычно около 2.22e-16

methods = {
    "цикл": mean_loop,
    "sum": mean_sum,
    "math.fsum": mean_fsum,
    "numpy.mean": mean_numpy,
}

print(f"N = {N}")
print(f"Машинное epsilon = {epsilon:.17e}")
print()

for name, mean in methods.items():
    diff = mean - mean_fsum
    print(
        f"{name:12s}: {mean:.17g}  "
        f"Δ от fsum = {diff:+.3e}  "
        f"|Δ| / epsilon = {abs(diff) / epsilon:.3g}"
    )

print("\nПопарные расхождения в единицах epsilon:")
names = list(methods)
for i, name_a in enumerate(names):
    for name_b in names[i + 1:]:
        difference = abs(methods[name_a] - methods[name_b])
        print(f"{name_a:12s} — {name_b:12s}: {difference / epsilon:.3g}")

print("\nОтносительное расхождение с math.fsum:")
for name, mean in methods.items():
    if mean_fsum != 0:
        relative = abs(mean - mean_fsum) / abs(mean_fsum)
        print(f"{name:12s}: {relative:.3e}")
