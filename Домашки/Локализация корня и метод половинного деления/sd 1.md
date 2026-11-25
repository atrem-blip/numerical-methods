def bisection(f, a, b, eps, max_iter=100):
    """Метод бисекции с журналом итераций.
    Возвращает (корень, журнал [(k, a, b, c, f(c), b-a)])."""
    if f(a) * f(b) > 0:
        raise ValueError("На отрезке нет смены знака!")

    log = []
    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        log.append((k, a, b, c, fc, b - a))

        # корень найден с нужной точностью
        if b - a < eps or abs(fc) < eps:
            return c, log

        # выбираем половину, где меняется знак
        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return c, log


f = lambda x: x**3 - 2*x - 5

# 1. Проверка смены знака
print("f(2) =", f(2), "  f(3) =", f(3))

# 3. Поиск корня с точностью eps = 1e-6
eps = 1e-6
root, log = bisection(f, 2, 3, eps)

print(f"{'k':>3} | {'a':>12} | {'b':>12} | {'c':>12} | {'f(c)':>12} | {'b-a':>12}")
for k, a, b, c, fc, width in log:
    print(f"{k:>3} | {a:>12.8f} | {b:>12.8f} | {c:>12.8f} | {fc:>12.8f} | {width:>12.8f}")

# 4. Проверка результата
print("\nКорень:", root)
print("f(корень) =", f(root))
print("|f(x)| < 1e-6:", abs(f(root)) < 1e-6)
