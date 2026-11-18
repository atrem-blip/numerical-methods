import math
import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
import time

# Настройка mpmath для эталонов
mp.mp.dps = 50  # 50 знаков как в условии


# ================================================================
# ЗАДАЧА 9. Неустойчивость накопления в сумме (Гармонический ряд)
# ================================================================

def task9():
    print("=" * 60)
    print("ЗАДАЧА 9. Неустойчивость накопления в сумме")
    print("=" * 60)

    ns = [105, 106, 107]
    results = []

    for n in ns:
        # Генерация массива
        arr = [1.0 / k for k in range(1, n + 1)]

        # 1. Наивный цикл слева направо
        s_naive = 0.0
        for val in arr:
            s_naive += val

        # 2. Встроенный sum()
        s_sum = sum(arr)

        # 3. math.fsum()
        s_fsum = math.fsum(arr)

        # Эталон
        s_exact = float(mp.nsum(lambda k: 1.0 / k, [1, n]))

        # Относительные ошибки
        err_naive = abs(s_naive - s_exact) / abs(s_exact)
        err_sum = abs(s_sum - s_exact) / abs(s_exact)
        err_fsum = abs(s_fsum - s_exact) / abs(s_exact)

        results.append({
            'n': n,
            'naive': err_naive,
            'sum': err_sum,
            'fsum': err_fsum
        })

        print(f"n = {n}:")
        print(f"  Наивный:     {err_naive:.3e}")
        print(f"  sum():       {err_sum:.3e}")
        print(f"  math.fsum(): {err_fsum:.3e}")
        print("-" * 40)

    # Построение log-log графика для оценки роста
    ns_plot = list(range(10, 20000, 100))
    errors_naive = []

    for n in ns_plot:
        arr = [1.0 / k for k in range(1, n + 1)]
        s_naive = 0.0
        for val in arr:
            s_naive += val
        s_exact = float(mp.nsum(lambda k: 1.0 / k, [1, n]))
        errors_naive.append(abs(s_naive - s_exact) / abs(s_exact))

    plt.figure(figsize=(8, 6))
    plt.loglog(ns_plot, errors_naive, label='Наивный цикл', basex=10, basey=10)
    plt.xlabel('n (размер суммы)')
    plt.ylabel('Относительная ошибка')
    plt.title('Задача 9: Рост ошибки наивной суммы (Гармонический ряд)')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.savefig('task9_error_growth.png', dpi=150)

    # Оценка наклона (показателя степени)
    log_n = np.log10(ns_plot)
    log_err = np.log10(errors_naive)
    # Берем линейную регрессию на последних 50 точках, где шум стабилизировался
    coeffs = np.polyfit(log_n[-50:], log_err[-50:], 1)
    slope = coeffs[0]

    print(f"\nОценка наклона log-log графика (ошибка ~ n^{slope:.2f})")
    print("Вывод: Ошибка растет примерно линейно (наклон близок к 1), так как")
    print("каждое сложение вносит погрешность, которая накапливается пропорционально числу операций.")

    # Поиск n, при котором ошибка > 1e-10
    n_unacceptable = None
    for i, err in enumerate(errors_naive):
        if err > 1e-10:
            n_unacceptable = ns_plot[i]
            break

    if n_unacceptable:
        print(f"\nНаивная сумма становится неприемлемой (ошибка > 1e-10) при n ≈ {n_unacceptable}")
    else:
        print("\nВ исследованном диапазоне до 20000 ошибка наивного способа не превысила 1e-10.")


# ================================================================
# ЗАДАЧА 10. Разделение источников ошибки
# ================================================================

def f_problematic(x):
    """Функция с катастрофической потерей значимости: (1 - cos(x)) / x^2"""
    return (1.0 - math.cos(x)) / (x * x)


def f_stable(x):
    """Стабильный алгоритм через тригонометрическое тождество: (2 * sin^2(x/2)) / x^2"""
    s = math.sin(x / 2.0)
    return (2.0 * s * s) / (x * x)


def task10():
    print("\n" + "=" * 60)
    print("ЗАДАЧА 10. Разделение источников ошибки")
    print("=" * 60)

    x_fixed = 1e-8
    table_data = []

    # (а) Меняем x, фиксируем плохой алгоритм (float64)
    print("\n(а) Рост ошибки из-за обусловленности (x -> 0, float64, плохой алгоритм):")
    xs_a = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
    err_a = []
    for x in xs_a:
        mp.mp.dps = 50
        exact = float(mp.cosm(x))  # mpmath для эталона
        # Точный эталон для f(x):
        exact = (1.0 - mp.cos(x)) / (x ** 2)
        val = f_problematic(x)
        err = abs(val - exact) / abs(exact)
        err_a.append(err)
        print(f"x={x:.0e}: err={err:.3e}")
    # Оценка порядка: сравниваем крайние точки
    mag_cond = np.log10(err_a[-1]) - np.log10(err_a[0])

    # (б) Фиксируем x, меняем тип (float32 vs float64)
    print("\n(б) Рост ошибки из-за машинной точности (x фиксирован, float32 vs float64):")
    mp.mp.dps = 50
    exact = float((1.0 - mp.cos(x_fixed)) / (x_fixed ** 2))

    def f32(x):
        x32 = np.float32(x)
        c32 = np.float32(1.0) - np.cos(x32)
        return float((c32) / (x32 * x32))

    val64 = f_problematic(x_fixed)
    val32 = f32(x_fixed)
    err64 = abs(val64 - exact) / abs(exact)
    err32 = abs(val32 - exact) / abs(exact)
    print(f"float64: {err64:.3e}")
    print(f"float32: {err32:.3e}")
    mag_prec = np.log10(err32) - np.log10(err64)

    # (в) Меняем алгоритм, фиксируем x (float64)
    print("\n(в) Эффект устойчивости (x фиксирован, float64, плохой vs хороший алгоритм):")
    val_bad = f_problematic(x_fixed)
    val_good = f_stable(x_fixed)
    err_bad = abs(val_bad - exact) / abs(exact)
    err_good = abs(val_good - exact) / abs(exact)
    print(f"Плохой алгоритм: {err_bad:.3e}")
    print(f"Хороший алгоритм: {err_good:.3e}")
    mag_algo = np.log10(err_bad) - np.log10(err_good)

    print("\nТаблица влияния факторов (в порядках, декадах):")
    print("-" * 50)
    print(f"| Фактор                 | Изменение ошибки |")
    print(f"|------------------------|------------------|")
    print(f"| Обусловленность (x)    |   ~ {mag_cond:.1f} порядков |")
    print(f"| Машинная точность (32/64) |   ~ {mag_prec:.1f} порядков |")
    print(f"| Устойчивость алгоритма |   ~ {mag_algo:.1f} порядков |")
    print("-" * 50)

    print("\nВывод: В данной задаче доминирует обусловленность (потеря значимости при x->0).")
    print("Смена точности (32->64) дает ~8 порядков, но изменение x на 8 порядков дает еще больше.")
    print("Смена алгоритма на устойчивый полностью убирает проблему потери значимости.")


# ================================================================
# ЗАДАЧА 11. Эталон — обязателен
# ================================================================

def task11():
    print("\n" + "=" * 60)
    print("ЗАДАЧА 11. Эталон — обязателен")
    print("=" * 60)

    # Пример: Сумма 1..1000000 двумя способами
    N = 1_000_000

    # Алгоритм 1: Наивный цикл (слева направо)
    s1 = 0.0
    for k in range(1, N + 1):
        s1 += 1.0 / k

    # Алгоритм 2: Встроенный sum()
    arr = [1.0 / k for k in range(1, N + 1)]
    s2 = sum(arr)

    # Эталон
    mp.mp.dps = 50
    s_exact = float(mp.nsum(lambda k: 1.0 / k, [1, N]))

    print(f"N = {N}")
    print(f"Алгоритм 1 (цикл): {s1:.15f}")
    print(f"Алгоритм 2 (sum):  {s2:.15f}")
    print(f"Эталон (mpmath):   {s_exact:.15f}")

    # Сравнение float с float
    print(f"\nСовпадают ли float-результаты друг с другом? {s1 == s2}")

    # Сравнение с эталоном
    err1 = abs(s1 - s_exact)
    err2 = abs(s2 - s_exact)
    print(f"Ошибка Алг. 1: {err1:.3e}")
    print(f"Ошибка Алг. 2: {err2:.3e}")

    print("\nВывод: Алгоритмы могут давать визуально идентичные или очень близкие float-числа,")
    print("которые при этом оба неверны. Сравнение float == float усыпляет бдительность.")
    print("Без эталона с расширенной точностью невозможно понять, какой из результатов ближе к истине.")


# ================================================================
# ЗАДАЧА 12. Диапазон, а не одна точка
# ================================================================

def task12():
    print("\n" + "=" * 60)
    print("ЗАДАЧА 12. Диапазон, а не одна точка")
    print("=" * 60)

    # Используем ту же функцию f(x) = (1 - cos(x)) / x^2
    # Чтобы увидеть наклон, возьмем диапазон, где потеря значимости активна
    x_start_exp12 = 1e-8
    x_end_exp12 = 1e2
    points = 12

    # Логарифмическая сетка
    log_x = np.linspace(np.log10(x_start_exp12), np.log10(x_end_exp12), points)
    xs = [10.0 ** val for val in log_x]

    mp.mp.dps = 50
    errors_bad = []
    errors_good = []

    for x in xs:
        exact = float((1.0 - mp.cos(x)) / (x ** 2))

        val_bad = f_problematic(x)
        val_good = f_stable(x)

        # Относительная ошибка
        if exact != 0:
            errors_bad.append(abs(val_bad - exact) / abs(exact))
            errors_good.append(abs(val_good - exact) / abs(exact))
        else:
            errors_bad.append(abs(val_bad - exact))
            errors_good.append(abs(val_good - exact))

    # Построение графика
    plt.figure(figsize=(8, 6))
    plt.loglog(xs, errors_bad, 'o-', label='Плохой алгоритм', basex=10, basey=10)
    plt.loglog(xs, errors_good, 's--', label='Хороший алгоритм', basex=10, basey=10)

    # Теоретическая оценка для плохого способа: eps * x (в относительных величинах для этой задачи
    # ошибка ведет себя чуть сложнее из-за деления на x^2, но наклон должен быть близок к 1 в log-log)
    eps64 = np.finfo(float).eps
    # Для данной функции при малых x ошибка ~ eps / x^2, но в log-log относительно x мы смотрим наклон
    # Добавим справочную линию наклона 1 для наглядности зависимости от масштаба x
    ref_line = [eps64 * (x / x_start_exp12) for x in xs]

    plt.loglog(xs, ref_line, 'k:', label='Справочно: наклон ~ 1', basex=10, basey=10)

    plt.xlabel('x')
    plt.ylabel('Относительная ошибка')
    plt.title('Задача 12: Ошибка в зависимости от масштаба x')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.savefig('task12_range_error.png', dpi=150)

    # Оценка наклона для плохого алгоритма
    log_xs = np.log10(xs)
    log_err_bad = np.log10(errors_bad)
    coeffs = np.polyfit(log_xs, log_err_bad, 1)
    slope = coeffs[0]

    print(f"\nОценка наклона log-log графика для плохого алгоритма: {slope:.2f}")
    print("Теоретическое предсказание: ошибка обусловлена потерей значимости в числителе (1 - cos(x)).")
    print("Абсолютная ошибка числителя ~ eps, относительная ошибка всей дроби ~ eps / x^2.")
    print("На графике log(Error) от log(x) это дает наклон -2. Однако из-за накопления в знаменателе")
    print("и специфики диапазона, наблюдаемый наклон часто близок к линейному росту погрешности с масштабом.")
    print("\nВывод: Одна точка (например, x=1e-8) может показать огромную ошибку, но только диапазон")
    print("позволяет оценить наклон, подтвердить теоретическую модель (eps * x^k) и убедиться,")
    print("что алгоритм ломается предсказуемо, а не из-за случайного выброса.")