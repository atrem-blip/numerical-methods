import math
from decimal import Decimal, getcontext


def naive_sqrt_diff(x: float) -> float:
    """
    Наивная реализация: катастрофическое вычитание близких чисел.
    При больших x значения sqrt(x+1) и sqrt(x) совпадают в большинстве значимых разрядов.
    """
    return math.sqrt(x + 1.0) - math.sqrt(x)


def stable_sqrt_diff(x: float) -> float:
    """
    Устойчивая реализация через сопряженное выражение.
    Алгебраическое преобразование: (a - b) = (a^2 - b^2) / (a + b)
    """
    return 1.0 / (math.sqrt(x + 1.0) + math.sqrt(x))


def high_precision_reference(x: float, precision: int = 50) -> float:
    """
    Независимый эталон высокой точности с использованием Decimal.
    """
    getcontext().prec = precision
    dx = Decimal(x)
    return float((dx + 1).sqrt() - dx.sqrt())


def run_experiment():
    # Диапазон: от малых до очень больших чисел
    test_values = [1.0, 10.0, 1.0e6, 1.0e12, 1.0e16]

    print(f"{'x':>15} | {'Naive':>25} | {'Stable':>25} | {'HighPrec(Ref)':>25} | {'Naive Rel Error':>18}")
    print("-" * 115)

    for x in test_values:
        ref = high_precision_reference(x)
        naive = naive_sqrt_diff(x)
        stable = stable_sqrt_diff(x)

        # Относительная ошибка наивного метода
        if ref != 0:
            naive_err = abs(naive - ref) / abs(ref)
        else:
            naive_err = float('inf')

        print(f"{x:15.2e} | {naive:25.16e} | {stable:25.16e} | {ref:25.16e} | {naive_err:18.2e}")


if __name__ == "__main__":
    run_experiment()