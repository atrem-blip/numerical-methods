import math

# Входные данные
ranges = 3
powers = [14, -16]
numbers = [1, 5, 15]

# 1. Генерация диапазонов: [10^(i-1), 10^i) для i от 1 до ranges
range_bounds = []
for i in range(1, ranges + 1):
    lower = 10 ** (i - 1)
    upper = 10 ** i
    range_bounds.append((lower, upper))

# 2. Вычисление степеней
power_results = [10 ** p for p in powers]

# 3. Форматирование чисел: добавление запятой как разделителя тысяч
formatted_numbers = [f"{n:,}" for n in numbers]

# Вывод результатов
print("Диапазоны:")
for i, (low, high) in enumerate(range_bounds, 1):
    print(f"{i}: [{low}, {high})")

print("\nСтепени:")
for p, val in zip(powers, power_results):
    print(f"10^{p} = {val}")

print("\nЧисла с разделителями:")
for n, f in zip(numbers, formatted_numbers):
    print(f"{n} -> {f}")

# Дополнительная проверка: в какой диапазон попадает каждое число
print("\nПроверка вхождения чисел в диапазоны:")
for n in numbers:
    found = False
    for i, (low, high) in enumerate(range_bounds, 1):
        if low <= n < high:
            print(f"{n} попадает в диапазон {i}: [{low}, {high})")
            found = True
            break
    if not found:
        print(f"{n} не попадает ни в один из заданных диапазонов")