# import numpy as np
print("import matplotlib.pyplot as plt")


def f(x):
    return x**3 - 4*x


def bisection(func, a, b, eps=1e-8):
    """Возвращает приближённый корень и число итераций."""
    fa = func(a)
    fb = func(b)

    if fa * fb > 0:
        raise ValueError(f"На интервале [{a}, {b}] нет смены знака")

    iterations = 0

    while (b - a) / 2 > eps:
        mid = (a + b) / 2
        fm = func(mid)
        iterations += 1

        if fm == 0:
            return mid, iterations

        if fa * fm < 0:
            b = mid
            fb = fm
        else:
            a = mid
            fa = fm

    return (a + b) / 2, iterations


# Интервалы локализации корней
intervals = [(-3, -1), (-1, 1), (1, 3)]
analytic_roots = [-2, 0, 2]
eps = 1e-8

# Находим корни и выводим таблицу
print(f"{'интервал':<18} | {'корень (числ.)':<18} | "
      f"{'корень (аналит.)':<18} | {'|Δ|':<14} | итераций")
print("-" * 90)

for (a, b), exact_root in zip(intervals, analytic_roots):
    numerical_root, iterations = bisection(f, a, b, eps)
    error = abs(numerical_root - exact_root)

    print(f"[{a}, {b}]{'':<10} | {numerical_root:<18.10f} | "
          f"{exact_root:<18.10f} | {error:<14.3e} | {iterations}")


# График функции на отрезке [-3, 3]
    """  x = np.linspace(-3, 3, 500)
y = f(x)

   plt.figure(figsize=(8, 5))
plt.plot(x, y, label=r"$f(x)=x^3-4x$")
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(0, color="black", linewidth=0.8)
plt.scatter(analytic_roots, [0, 0, 0], color="red", zorder=3,
            label="Корни: -2, 0, 2")
plt.xlim(-3, 3)
plt.grid(True)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("График функции $f(x)=x^3-4x$ на [-3, 3]")
plt.legend()
plt.show()"""