import timeit
# import matplotlib.pyplot as plt

def run_benchmark():
    # Параметры
    sizes = [100, 1_000, 10_000, 100_000]
    number = 1000  # проверок в одном замере
    repeat = 5     # повторов timeit
    target = -1    # число, которого нет в коллекциях (худший случай для list)

    # Хранилища для результатов
    results = []

    for n in sizes:
        # Подготовка данных
        data_list = list(range(n))
        data_set = set(range(n))
        data_dict = {i: i for i in range(n)}

        # Замер для list
        list_times = timeit.repeat(
            stmt="target in data",
            setup="pass",
            repeat=repeat,
            number=number,
            globals={"target": target, "data": data_list}
        )
        list_us = (min(list_times) / number) * 1_000_000

        # Замер для set
        set_times = timeit.repeat(
            stmt="target in data",
            setup="pass",
            repeat=repeat,
            number=number,
            globals={"target": target, "data": data_set}
        )
        set_us = (min(set_times) / number) * 1_000_000

        # Замер для dict (проверка ключей)
        dict_times = timeit.repeat(
            stmt="target in data",
            setup="pass",
            repeat=repeat,
            number=number,
            globals={"target": target, "data": data_dict}
        )
        dict_us = (min(dict_times) / number) * 1_000_000

        # Расчёт ускорений
        set_vs_list = list_us / set_us if set_us > 0 else float('inf')
        dict_vs_list = list_us / dict_us if dict_us > 0 else float('inf')

        results.append({
            'n': n,
            'list_us': list_us,
            'set_us': set_us,
            'dict_us': dict_us,
            'set_vs_list': set_vs_list,
            'dict_vs_list': dict_vs_list
        })

    # Печать таблицы
    print(f"{'n':>10} | {'list (мкс)':>12} | {'set (мкс)':>12} | {'dict (мкс)':>12} | {'set/list':>10} | {'dict/list':>10}")
    print("-" * 70)
    for r in results:
        print(f"{r['n']:>10} | {r['list_us']:>12.3f} | {r['set_us']:>12.3f} | {r['dict_us']:>12.3f} | {r['set_vs_list']:>10.2f} | {r['dict_vs_list']:>10.2f}")

    # Построение графика
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot([r['n'] for r in results], [r['list_us'] for r in results], marker='o', label='list')
    ax.plot([r['n'] for r in results], [r['set_us'] for r in results], marker='o', label='set')
    ax.plot([r['n'] for r in results], [r['dict_us'] for r in results], marker='o', label='dict')

    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlabel('Размер коллекции n')
    ax.set_ylabel('Время одной проверки (мкс, лог-шкала)')
    ax.set_title('Сравнение скорости поиска: list vs set vs dict')
    ax.legend()
    ax.grid(True, which="both", alpha=0.2)

    # Сохранение графика
    plt.tight_layout()
    plt.savefig("hw1_search.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    run_benchmark()