
# -*- coding: utf-8 -*-
"""
Мини-отчёт: задачи 13-15
Воспроизводимость эксперимента, границы представимости float,
полный корректный численный эксперимент.

Всё печатается в консоль: каждая задача - отдельный раздел
с целью, методикой, таблицей результатов и выводом.
"""

import math
import random
import platform

import numpy as np

try:
    import mpmath
    HAVE_MPMATH = True
except ImportError:
    HAVE_MPMATH = False

LINE = "=" * 78


def header(title):
    print("\n" + LINE)
    print(title)
    print(LINE)


def print_env():
    header("ОКРУЖЕНИЕ (данные для отчёта)")
    print("Python :", platform.python_version())
    print("NumPy  :", np.__version__)
    if HAVE_MPMATH:
        print("mpmath :", mpmath.__version__)
    print("Платформа:", platform.platform())


# =====================================================================
# ЗАДАЧА 13. Воспроизводимость эксперимента
# =====================================================================

N = 100_000  # 10^5 случайных чисел (в условии "105" читаем как 1e5)

SEEDS = (42, 43)
METHODS = ("sum", "fsum", "np.sum")


def gen_python(seed):
    random.seed(seed)
    return [random.random() for _ in range(N)]


def gen_numpy(seed):
    return np.random.default_rng(seed).random(N)


def naive_loop_sum(seq):
    acc = 0.0
    for x in seq:
        acc += x  # честное последовательное накопление ошибок округления
    return acc


def measure(seq):
    if isinstance(seq, np.ndarray):
        seq_list = seq.tolist()
    else:
        seq_list = list(seq)
    return {
        "наивный цикл": naive_loop_sum(seq_list),
        "sum": float(sum(seq_list)),
        "fsum": float(math.fsum(seq_list)),
        "np.sum": float(np.sum(seq)),
    }


METHODS = ("наивный цикл", "sum", "fsum", "np.sum")


def task13():
    header("ЗАДАЧА 13. Воспроизводимость: seed=42 (два прогона) и seed=43")
    print(f"Объём выборки: N = {N} чисел на отрезке [0, 1)")
    print("Генераторы: random.seed(s)+random.random() и np.random.default_rng(s)")
    print("Способы: наивный цикл acc+=x, встроенный sum, math.fsum, np.sum")
    print()
    print("Примечание: в Python 3.12+ встроенный sum для float использует")
    print("компенсированное суммирование (Neumaier), поэтому он совпадает")
    print("с fsum - это само по себе аргумент о зависимости от версии Python.")
    print()

    results = {}
    for gen_name, gen in (("random", gen_python), ("numpy", gen_numpy)):
        for seed in SEEDS:
            r1, r2 = measure(gen(seed)), measure(gen(seed))
            identical = all(r1[m] == r2[m] for m in METHODS)
            results[(gen_name, seed)] = r1
            print(f"Генератор {gen_name:6s} | seed={seed} | прогон 1 == прогон 2: {identical}")
            for m in METHODS:
                dev = r1[m] - r1["fsum"]
                rel = abs(dev) / abs(r1["fsum"])
                print(f"    {m:12s}: {r1[m]!r:24s} отклонение от fsum: {dev:+.3e} (отн. {rel:.2e})")
            print()

    print("Таблица 'систематичности' расхождений (относительная ошибка отн. fsum):")
    print(f"{'генератор':10s} {'seed':>5s} {'наивный цикл':>14s} {'sum':>14s} {'np.sum':>14s}")
    for gen_name in ("random", "numpy"):
        for seed in SEEDS:
            r = results[(gen_name, seed)]
            fs = r["fsum"]
            e_loop = abs(r["наивный цикл"] - fs) / abs(fs)
            e_sum = abs(r["sum"] - fs) / abs(fs)
            e_np = abs(r["np.sum"] - fs) / abs(fs)
            print(f"{gen_name:10s} {seed:5d} {e_loop:14.3e} {e_sum:14.3e} {e_np:14.3e}")

    print("""
ВЫВОД (задача 13):
1. При фиксированном seed оба генератора выдают одинаковые последовательности,
   и все способы дают бит-в-бит одинаковые суммы в повторном прогоне
   (отклонение ровно 0). Эксперимент воспроизводим.
2. Расхождения между способами НЕ случайны: относительная ошибка наивного
   цикла (~1e-14, абсолютная ~1e-10) воспроизводится по порядку величины для seed=42
   и seed=43. Это накопление ошибок округления float64 за O(N) сложений.
   np.sum (попарная схема, O(log N)) и fsum (алгоритм Шевчука) дают
   практически точный результат (~1e-16).
3. Отдельный урок: встроенный sum в Python 3.12 уже компенсированный
   (Neumaier) и потому совпал с fsum - на Python 3.11 тот же код дал бы
   другие числа. Результат зависит от версии интерпретатора.
4. Без фиксации seed меняются сами данные; без фиксации версий Python/NumPy
   меняются ГСЧ, компенсация в sum и порядок операций в pairwise-суммировании.
   Вывод: seed + версии окружения обязательны для воспроизводимости.
""")


# =====================================================================
# ЗАДАЧА 14. Границы представимости
# =====================================================================

def fmt(v):
    if isinstance(v, str):
        return v
    if math.isnan(v):
        return "nan"
    if math.isinf(v):
        return "inf" if v > 0 else "-inf"
    return f"{v:.6g}"


def task14():
    header("ЗАДАЧА 14. Границы представимости: sum / fsum / np.sum")

    BIG, SMALL, ZERO, DENORM = 1e300, 1e-300, 0.0, 1e-320
    INF, NEG_INF, NAN = float("inf"), float("-inf"), float("nan")

    cases = [
        ("смесь масштабов: 1e300,1e300,1e-300,0,1e-320",
         [BIG, BIG, SMALL, ZERO, DENORM]),
        ("переполнение: 1.7e308 + 1.7e308", [1.7e308, 1.7e308]),
        ("смесь масштабов + nan", [BIG, SMALL, ZERO, DENORM, NAN]),
        ("смесь масштабов + inf", [BIG, SMALL, ZERO, DENORM, INF]),
        ("inf и -inf", [INF, NEG_INF]),
        ("мелкие: 1e-300, 1e-320, 0.0", [SMALL, DENORM, ZERO]),
    ]

    w = 46
    print(f"{'случай':{w}s} | {'sum':>14s} | {'fsum':>14s} | {'np.sum':>14s}")
    print("-" * (w + 50))
    for name, seq in cases:
        try:
            r_sum = fmt(float(sum(seq)))
        except Exception as e:
            r_sum = f"ERR:{type(e).__name__}"
        try:
            r_fsum = fmt(float(math.fsum(seq)))
        except Exception as e:
            r_fsum = f"ERR:{type(e).__name__}"
        with np.errstate(invalid="ignore", over="ignore"):
            try:
                r_np = fmt(float(np.sum(seq)))
            except Exception as e:
                r_np = f"ERR:{type(e).__name__}"
        print(f"{name:{w}s} | {r_sum:>14s} | {r_fsum:>14s} | {r_np:>14s}")

    print("""
Разбор поведения:
- Переполнение: 1.7e308 + 1.7e308 = 3.4e308 > max double (~1.797e308).
  sum и np.sum "молча" возвращают inf; fsum, заметив переполнение
  ПРОМЕЖУТОЧНОЙ точной суммы, честно бросает OverflowError.
- Смесь 1e300 + 1e300 = 2e300 переполнения НЕ даёт, но 1e-300 и
  денормализованные 1e-320 рядом с 1e300 полностью "проглатываются":
  они меньше последнего бита мантиссы числа 1e300 (2^(-1022) ~ 2e-308).
- Денормализованные (~1e-320) имеют мантиссу короче 53 бит, поэтому сами
  по себе неточны; в сумме с обычными числами почти не видны.
- NaN: sum, fsum и np.sum дают nan - "заражение" распространилось на
  весь результат. Отличие: по итоговой сумме нельзя понять, ГДЕ появился
  NaN; np.nansum молча выбрасывает NaN - отдельный источник ошибок.
- fsum при наличии inf: fsum([inf, 1e300, ...]) возвращает inf (inf -
  корректный точный результат), но fsum([inf, -inf]) бросает ValueError:
  точная арифметика не может разрешить inf - inf, и fsum отказывается
  молча выдать неопределённость. sum и np.sum дают nan (np.sum ещё и
  пишет RuntimeWarning).

ВЫВОД: как обрабатывать граничные значения в реальном коде:
1. Проверяйте входы до вычисления: np.isfinite(x).all() или явный разбор
   inf/nan с политикой обработки (ошибка / исключение / nansum).
2. Переполнение ловите как OverflowError от fsum либо проверяйте
   math.isinf(result) - "тихий inf" опаснее исключения.
3. Не смешивайте в одном массиве порядки 1e300 и 1e-300: мелкие слагаемые
   не учитываются вовсе - масштабируйте или логарифмируйте данные.
4. Денормалы сравнивайте с нулём через abs(x) < eps, а не == 0.
""")


# =====================================================================
# ЗАДАЧА 15. Полный корректный эксперимент
# Функция: g(x) = (1 - cos x) / x^2   (предел при x->0 равен 1/2)
# Плохой алгоритм: прямое вычисление формулы (катастрофическая отмена)
# Хороший алгоритм: тождество 1 - cos x = 2 sin^2(x/2)  ->  2 sin^2(x/2)/x^2
# Эталон: mpmath, 50 значащих цифр
# =====================================================================

def naive_g(x):
    return (1.0 - math.cos(x)) / x ** 2


def good_g(x):
    s = math.sin(x / 2.0)
    return 2.0 * s * s / x ** 2


def task15():
    header("ЗАДАЧА 15. Полный корректный эксперимент: g(x) = (1 - cos x)/x^2")
    print("""
ЦЕЛЬ: показать, что наивная формула теряет точность при малых x из-за
      катастрофической отмены в 1 - cos(x), и что исправленная формула
      восстанавливает точность до машинного эпсилон.
ПОСТАНОВКА: для сетки x = 10^k, k = 0..-9 (10 точек, логарифмическая сетка),
      вычислить g(x) тремя способами и посчитать относительную ошибку
      от эталона.
ЭТАЛОН: mpmath, 50 знаков точности; истинное значение lim g(x) = 0.5.
""")

    if not HAVE_MPMATH:
        print("mpmath недоступен - эксперимент прерван.")
        return

    mpmath.mp.dps = 50

    def ref_g(x):
        xm = mpmath.mpf(x)
        return float((1 - mpmath.cos(xm)) / xm ** 2)

    xs = [10.0 ** k for k in range(0, -10, -1)]
    w1, w2, w3, w4 = 10, 22, 22, 22
    print(f"{'x':>{w1}s} | {'наивный':>{w2}s} | {'хороший':>{w3}s} | {'эталон':>{w4}s} | {'ошибка наивного':>16s} | {'ошибка хорошего':>16s}")
    print("-" * (w1 + w2 + w3 + w4 + 45))
    for x in xs:
        ref = ref_g(x)
        nv, gd = naive_g(x), good_g(x)
        e_nv = abs(nv - ref) / abs(ref)
        e_gd = abs(gd - ref) / abs(ref)
        print(f"{x:>{w1}.0e} | {nv:>{w2}.17g} | {gd:>{w3}.17g} | {ref:>{w4}.17g} | {e_nv:16.2e} | {e_gd:16.2e}")

    print("""
ВЫВОД (задача 15):
1. Граница устойчивости наивного алгоритма: пока 1 - cos(x) значительно
   больше машинного эпсилон (то есть x >~ 1e-7), относительная ошибка
   растёт примерно как eps/x^2 (каждый потерянный разряд в 1 - cos(x)
   усиливается делением на x^2).
   При x ~ 1e-8 наивная формула даёт ошибку 100%: 1 - cos(x) целиком
   состоит из шума округления cos(x) (на практике получился 0.0).
2. Хороший алгоритм 2*sin^2(x/2)/x^2 держит относительную ошибку на уровне
   1-2 ulp (~1e-16) во всём диапазоне вплоть до x = 1e-9: sin(x/2)
   вычисляется с полной точностью, отмена отсутствует.
3. Достижимая точность: для корректной формулы - машинный эпсилон;
   для наивной формула пригодна только при |x| >~ 1e-6.
4. Урок: неустойчивость лечится алгебраическим преобразованием выражения
   (устранение отмены), а не "более точными" типами данных. Эталон высокой
   точности (mpmath/decimal) обязателен: без него наивный результат при
   x=1e-6 (0.500044...) выглядит правдоподобно, хотя уже неверен в 4-м знаке.
""")


def main():
    print_env()
    task13()
    task14()
    task15()
    header("КОНЕЦ ОТЧЁТА")


if __name__ == "__main__":
    main()
