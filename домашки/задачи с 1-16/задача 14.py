import math
import matplotlib.pyplot as plt

N = 10_000
factor = 1.0001
thresholds = (1e-9, 1e-6, 1e-3)

# Эталонное значение
reference = math.exp(N * math.log(factor))

# Итерационное вычисление и относительная погрешность на каждом шаге
x = 1.0
steps = []
errors = []
first_crossing = {threshold: None for threshold in thresholds}

for step in range(1, N + 1):
    x *= factor
    error = abs(x - math.exp(step * math.log(factor))) / math.exp(
        step * math.log(factor)
    )

    steps.append(step)
    errors.append(error)

    for threshold in thresholds:
        if first_crossing[threshold] is None and error > threshold:
            first_crossing[threshold] = step

print(f"Итерационный результат: {x:.17g}")
print(f"Эталонный результат:    {reference:.17g}")
print(f"Итоговая относительная погрешность: {errors[-1]:.6e}")

for threshold, step in first_crossing.items():
    if step is None:
        print(f"Порог {threshold:g}: не превышен")
    else:
        print(f"Порог {threshold:g}: впервые превышен на шаге {step}")

plt.figure(figsize=(10, 6))
plt.plot(steps, errors, linewidth=1, label="Относительная погрешность")
for threshold in thresholds:
    plt.axhline(threshold, linestyle="--", label=f"Порог {threshold:g}")

plt.yscale("log")
plt.xlabel("Номер шага")
plt.ylabel("Относительная погрешность")
plt.title("Накопление погрешности при многократном умножении")
plt.grid(True, which="both", linestyle=":")
plt.legend()
plt.tight_layout()
plt.show()
