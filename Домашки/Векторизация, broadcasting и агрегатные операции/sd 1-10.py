import numpy as np
import math
import time
import sys


def benchmark(func, *args, number=1):
    """Замер времени выполнения функции."""
    start = time.perf_counter()
    for _ in range(number):
        func(*args)
    end = time.perf_counter()
    return end - start


def task1_sum():
    print("\n=== Задача 1. Сумма массива ===")
    ns = [10 ** 5, 10 ** 6, 10 ** 7]
    results = []

    for n in ns:
        a = np.random.rand(n)

        # Python цикл
        def py_sum():
            s = 0.0
            for x in a:
                s += x
            return s

        # NumPy
        def np_sum():
            return a.sum()

        t_py = benchmark(py_sum)
        t_np = benchmark(np_sum)

        speedup = t_py / t_np if t_np > 0 else float('inf')
        results.append((n, speedup))
        print(f"n={n:,}: Python={t_py:.4f} с, NumPy={t_np:.4f} с, ускорение={speedup:.2f}x")

    print("\nТаблица n -> ускорение:")
    for n, sup in results:
        print(f"{n} -> {sup:.2f}x")

    # Оценка порога 10x
    for n, sup in results:
        if sup > 10:
            print(f"\nВывод: разница становится заметной (>10x) при n = {n}")
            break


def task2_mean_std():
    print("\n=== Задача 2. Среднее и стандартное отклонение ===")
    n = 10 ** 6
    a = np.random.rand(n)

    def py_stats():
        s = 0.0
        s2 = 0.0
        for x in a:
            s += x
            s2 += x * x
        mean = s / n
        # Смещенная дисперсия (как в np.std по умолчанию)
        var = s2 / n - mean * mean
        if var < 0: var = 0.0  # защита от отрицательного нуля из-за float errors
        std = math.sqrt(var)
        return mean, std

    np_mean = a.mean()
    np_std = a.std()

    py_mean, py_std = py_stats()

    match_mean = np.allclose(py_mean, np_mean, atol=1e-12)
    match_std = np.allclose(py_std, np_std, atol=1e-12)

    print(f"Python mean: {py_mean:.15f}, NumPy mean: {np_mean:.15f}, совпадают: {match_mean}")
    print(f"Python std:  {py_std:.15f}, NumPy std:  {np_std:.15f}, совпадают: {match_std}")


def task3_transform():
    print("\n=== Задача 3. Поэлементное преобразование ===")
    n = 10 ** 6
    a = np.random.rand(n)

    def py_transform():
        return [math.sin(x) + x * x for x in a]

    def np_transform():
        return np.sin(a) + a ** 2

    t_py = benchmark(py_transform)
    t_np = benchmark(np_transform)

    print(f"Python (list comp): {t_py:.4f} с")
    print(f"NumPy (vectorized): {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


def task4_clipping():
    print("\n=== Задача 4. Условная замена (clipping) ===")
    n = 10 ** 6
    # Генерируем данные с выбросами за пределы [0, 1]
    a = np.random.randn(n) * 0.5 + 0.5

    def py_clip():
        res = []
        for x in a:
            if x < 0:
                res.append(0.0)
            elif x > 1:
                res.append(1.0)
            else:
                res.append(x)
        return res

    def np_clip():
        return np.clip(a, 0, 1)

    # Статистика изменений для NumPy (как эталон)
    changed_count = np.sum((a < 0) | (a > 1))

    t_py = benchmark(py_clip)
    t_np = benchmark(np_clip)

    print(f"Элементов вне [0, 1]: {int(changed_count):,}")
    print(f"Python (цикл+if): {t_py:.4f} с")
    print(f"NumPy (clip):     {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


def task5_row_sum():
    print("\n=== Задача 5. Сумма по строкам ===")
    n = 10 ** 5
    m = np.random.rand(n, 10)

    def py_row_sum():
        res = [0.0] * n
        for i in range(n):
            s = 0.0
            for j in range(10):
                s += m[i, j]
            res[i] = s
        return res

    def np_row_sum():
        return m.sum(axis=1)

    t_py = benchmark(py_row_sum)
    t_np = benchmark(np_row_sum)

    print(f"Python (2 цикла): {t_py:.4f} с")
    print(f"NumPy (axis=1):   {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")
    print(f"SLOC (ориентир): Python ~6-8 строк, NumPy ~1 строка")


def task6_col_mean_norm():
    print("\n=== Задача 6. Среднее по столбцам и нормировка ===")
    n = 10 ** 5
    m = np.random.rand(n, 10)

    def py_norm():
        res = np.empty_like(m)
        # Вычисляем средние по столбцам (axis=0)
        col_means = [0.0] * m.shape[1]
        for j in range(m.shape[1]):
            s = 0.0
            for i in range(m.shape[0]):
                s += m[i, j]
            col_means[j] = s / m.shape[0]

        # Вычитаем (векторизация по строкам через broadcasting)
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                res[i, j] = m[i, j] - col_means[j]
        return res

    def np_norm():
        return m - m.mean(axis=0)

    t_py = benchmark(py_norm)
    t_np = benchmark(np_norm)

    print(f"Python (циклы): {t_py:.4f} с")
    print(f"NumPy (broadcasting): {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


def task7_max_argmax():
    print("\n=== Задача 7. Поиск максимума и индекса ===")
    n = 10 ** 6
    a = np.random.rand(n)

    def py_max():
        max_val = a[0]
        max_idx = 0
        for i, x in enumerate(a):
            if x > max_val:
                max_val = x
                max_idx = i
        return max_val, max_idx

    def np_max():
        return a.max(), a.argmax()

    t_py = benchmark(py_max)
    t_np = benchmark(np_max)

    val_py, idx_py = py_max()
    val_np, idx_np = np_max()

    print(f"Python: val={val_py:.6f}, idx={idx_py}")
    print(f"NumPy:  val={val_np:.6f}, idx={idx_np}")
    print(f"Python: {t_py:.4f} с, NumPy: {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


def task8_filter_threshold():
    print("\n=== Задача 8. Фильтрация по порогу ===")
    n = 10 ** 6
    a = np.random.randn(n)

    def py_filter():
        return [x for x in a if x > 0]

    def np_filter():
        return a[a > 0]

    # Оценка памяти (примерная, размер указателей + объекты float)
    py_mem = sys.getsizeof([x for x in a if x > 0])
    np_mem = a[a > 0].nbytes

    t_py = benchmark(py_filter)
    t_np = benchmark(np_filter)

    print(f"Результат Python (len): {len(py_filter()):,}")
    print(f"Результат NumPy (len):  {len(np_filter()):,}")
    print(f"Память Python (оценка): ~{py_mem / 1024 ** 2:.2f} МБ")
    print(f"Память NumPy (точно):   {np_mem / 1024 ** 2:.2f} МБ")
    print(f"Python: {t_py:.4f} с, NumPy: {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


def task9_inplace_abs():
    print("\n=== Задача 9. Замена по маске (in-place) ===")
    n = 10 ** 6
    a_py = np.random.randn(n)
    a_np = a_py.copy()

    def py_abs_inplace():
        for i in range(len(a_py)):
            if a_py[i] < 0:
                a_py[i] = -a_py[i]

    def np_mask_inplace():
        a_np[a_np < 0] *= -1
        # Альтернатива: np.abs(a_np, out=a_np)

    t_py = benchmark(py_abs_inplace)
    t_np = benchmark(np_mask_inplace)

    # Проверка идентичности результата
    identical = np.array_equal(a_py, a_np)

    print(f"Python (цикл): {t_py:.4f} с")
    print(f"NumPy (маска): {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")
    print(f"Результаты идентичны: {identical}")


def task10_combined_mask():
    print("\n=== Задача 10. Комбинированная маска ===")
    n = 10 ** 6
    a = np.random.randn(n)

    def py_filter():
        return [x for x in a if -1 < x < 1]

    def np_filter():
        # Скобки обязательны из-за приоритета операторов в NumPy
        return a[(a > -1) & (a < 1)]

    t_py = benchmark(py_filter)
    t_np = benchmark(np_filter)

    print(f"Результат Python (len): {len(py_filter()):,}")
    print(f"Результат NumPy (len):  {len(np_filter()):,}")
    print(f"Python: {t_py:.4f} с, NumPy: {t_np:.4f} с")
    print(f"Ускорение: {t_py / t_np:.2f}x")


if __name__ == "__main__":
    task1_sum()
    task2_mean_std()
    task3_transform()
    task4_clipping()
    task5_row_sum()
    task6_col_mean_norm()
    task7_max_argmax()
    task8_filter_threshold()
    task9_inplace_abs()
    task10_combined_mask()