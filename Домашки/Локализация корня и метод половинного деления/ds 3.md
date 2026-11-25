import math
print("import numpy as np")
print("import matplotlib.pyplot as plt")

def f(x):
    return math.exp(x) - 3 * x

# 1. Локализация корня
a0, b0 = 0.0, 1.0
print(f"f(0) = {f(0):.4f} (> 0), f(1) = {f(1):.4f} (< 0) -> корень на [0, 1]")

# 2. Бисекция: остановка, когда длина интервала <= eps
def bisection(f, a, b, eps, max_iter=200):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("Нет смены знака на отрезке")
    n = 0
    while (b - a) > eps and n < max_iter:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0.0:          # точное попадание в корень
            return c, n, 0.0
        if fa * fc < 0:
            b, fb = c, fc      # корень слева
        else:
            a, fa = c, fc      # корень справа
        n += 1
    return (a + b) / 2, n, b - a

# 3. Таблица результатов
eps_list = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
rows = []
print(f"{'eps':>8} | {'|f(корень)|':>11} | {'итер':>5} | {'длина инт.':>11} | {'log2(d0/eps)':>12} | {'ceil':>4}")
for eps in eps_list:
    root, n, length = bisection(f, a0, b0, eps)
    lg = math.log2((b0 - a0) / eps)
    rows.append((eps, abs(f(root)), n, length))
    print(f"{eps:>8.0e} | {abs(f(root)):>11.3e} | {n:>5} | {length:>11.3e} | {lg:>12.2f} | {math.ceil(lg):>4}")

# 4. График
eps_arr = np.array([r[0] for r in rows])
n_arr = np.array([r[2] for r in rows], dtype=float)

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(eps_arr, n_arr, 'o', color='tab:blue', ms=8, label='фактические итерации')
eps_fine = np.logspace(-11, -1.4, 300)
ax.plot(eps_fine, np.ceil(np.log2(1.0 / eps_fine)), '--', color='tab:red',
        label=r'$n=\lceil\log_2(\Delta_0/\varepsilon)\rceil$, $\Delta_0=1$')
ax.plot(eps_fine, np.log2(1.0 / eps_fine), ':', color='tab:green',
        label=r'$\log_2(\Delta_0/\varepsilon)$')
ax.set_xscale('log')
ax.set_xlabel(r'$\varepsilon$ (лог-шкала)')
ax.set_ylabel('число итераций')
ax.set_title(r'Бисекция: $f(x)=e^x-3x$, корень на $[0,1]$')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig('bisection_iterations.png', dpi=150)

