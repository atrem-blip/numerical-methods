# hw2_squares.py
import timeit
import tracemalloc
# import matplotlib.pyplot as plt
# import numpy as np


def measure_time_and_memory(N):
    methods = {
        'Цикл с append': '''
result = []
for i in range(N):
    result.append(i * i)
''',
        'List comprehension': '''
result = [i * i for i in range(N)]
''',
        'map + lambda': '''
result = list(map(lambda i: i * i, range(N)))
'''
    }

    results = []

    for name, code in methods.items():
        # Замер времени
        timer = timeit.Timer(stmt=code, globals={'N': N})
        times = timer.repeat(repeat=5, number=1)
        time_min = min(times)

        # Замер пиковой памяти
        tracemalloc.start()
        exec(code, {'N': N})
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        # Переводим в МБ
        peak_mb = peak / (1024 * 1024)

        results.append({
            'method': name,
            'time_s': time_min,
            'peak_mb': peak_mb
        })

    return results


def main():
    sizes = [50_000, 200_000, 800_000]
    method_names = ['Цикл с append', 'List comprehension', 'map + lambda']

    # Словари для накопления данных по методам
    time_data = {name: [] for name in method_names}
    mem_data = {name: [] for name in method_names}

    for N in sizes:
        res = measure_time_and_memory(N)
        for r in res:
            time_data[r['method']].append(r['time_s'])
            mem_data[r['method']].append(r['peak_mb'])

    # Печать текстовой таблицы
    print(f"{'Метод':<20} | {'N':>10} | {'Время (с)':>10} | {'Память (МБ)':>12}")
    print("-" * 60)
    for i, N in enumerate(sizes):
        for name in method_names:
            print(f"{name:<20} | {N:>10,} | {time_data[name][i]:>10.4f} | {mem_data[name][i]:>12.2f}")

    # Построение дашборда
    x = np.arange(len(sizes))
    width = 0.25

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # График 1: Время (линии)
    for i, name in enumerate(method_names):
        ax1.plot(x, time_data[name], marker='o', label=name)

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"N={n:,}".replace(',', ' ') for n in sizes])
    ax1.set_xlabel("Размер N")
    ax1.set_ylabel("Время (секунды)")
    ax1.set_title("Время выполнения")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График 2: Память (группированные столбцы)
    for i, name in enumerate(method_names):
        ax2.bar(x + i * width, mem_data[name], width, label=name)

    ax2.set_xticks(x + width)
    ax2.set_xticklabels([f"N={n:,}".replace(',', ' ') for n in sizes])
    ax1.set_xlabel("Размер N")  # Подпись общая для наглядности, можно убрать
    ax2.set_ylabel("Пиковая память (МБ)")
    ax2.set_title("Потребление памяти")
    ax2.legend()
    ax2.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("hw2_squares.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()