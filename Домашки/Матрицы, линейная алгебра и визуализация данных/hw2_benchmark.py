import timeit
import tracemalloc
import matplotlib.pyplot as plt

# --- Три фрагмента для timeit ---
# Многострочный код в timeit допустим, отступы корректные
stmts = {
    "for + append": "out = []\nfor i in range(N):\n    out.append(i*i)",
    "list comprehension": "out = [i*i for i in range(N)]",
    "map + lambda": "out = list(map(lambda i: i*i, range(N)))",
}

N_values = [200_000, 500_000, 800_000]

times = {name: [] for name in stmts}        # минимальное время, сек
peaks = {name: [] for name in stmts}        # пиковая память, МБ

for N in N_values:
    for name, stmt in stmts.items():
        # --- Время: number=1, repeat=5, берём min ---
        t = min(timeit.repeat(stmt, repeat=5, number=1, globals={"N": N}))
        times[name].append(t)

        # --- Память: tracemalloc.start() -> exec -> get_traced_memory() -> stop() ---
        tracemalloc.start()
        exec(stmt, {"N": N})
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks[name].append(peak / (1024 * 1024))  # перевод в МБ

# --- Дашборд ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Слева: время
for name in stmts:
    ax1.plot(N_values, times[name], "o-", label=name)
ax1.set_xlabel("N (размер списка)")
ax1.set_ylabel("Время, с (min из 5 замеров)")
ax1.set_title("Время создания списка из N квадратов")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Справа: группированные столбцы по памяти
x = range(len(N_values))
width = 0.25
colors = ["tab:blue", "tab:orange", "tab:green"]
for i, name in enumerate(stmts):
    ax2.bar([xi + (i - 1) * width for xi in x], peaks[name],
            width=width, label=name, color=colors[i])
ax2.set_xticks(list(x))
ax2.set_xticklabels([f"N={N}" for N in N_values])
ax2.set_xlabel("Размер списка")
ax2.set_ylabel("Пиковая память, МБ")
ax2.set_title("Пиковая память (tracemalloc)")
ax2.legend()
ax2.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("hw2_dashboard.png", dpi=150)
plt.close()

# --- Вывод ---
print("=" * 60)
print(f"{'Способ':<20}{'N=200k, c':>11}{'N=500k, c':>11}{'N=800k, c':>11}{'Память @800k, МБ':>17}")
print("-" * 60)
for name in stmts:
    print(f"{name:<20}{times[name][0]:>11.4f}{times[name][1]:>11.4f}{times[name][2]:>11.4f}{peaks[name][2]:>17.1f}")
print("=" * 60)
print("ВЫВОД:")
print("1) Пиковая память у всех трёх способов практически одинаковая:")
print("   результат — один и тот же список на N int, а промежуточные")
print("   объекты (аргументы append, кадры вызовов lambda) краткоживущие")
print("   и на пик почти не влияют. Память определяется результатом,")
print("   а не способом его получения.")
print("2) List comprehension быстрее цикла с append: цикл исполняется")
print("   на уровне C без вызова метода out.append на каждой итерации.")
print("3) map + lambda медленнее: lambda — полноценная Python-функция,")
print("   и её вызов на каждый элемент дороже встроенной операции,")
print("   плюс накладные расходы самого итератора map.")
print("4) Генератор вместо списка ((i*i for i in range(N))) снизил бы")
print("   пиковую память до константы (сотни байт): элементы вычисляются")
print("   по требованию. Но время суммирования такого генератора")
print("   сопоставимо с циклом — он тоже интерпретируется поэлементно.")
