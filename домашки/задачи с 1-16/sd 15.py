from decimal import Decimal, getcontext

getcontext().prec = 28

operations = 10**6
kopecks_per_operation = 1  # начисляем 0,01 рубля

# (а) float
balance_float = 0.0
for _ in range(operations):
    balance_float += 0.01

# (б) Decimal
balance_decimal = Decimal("0")
for _ in range(operations):
    balance_decimal += Decimal("0.01")

# (в) целые копейки
balance_kopecks = 0
for _ in range(operations):
    balance_kopecks += kopecks_per_operation
balance_int = Decimal(balance_kopecks) / Decimal(100)

# Точное значение для сравнения
exact = Decimal(operations) / Decimal(100)

# Расхождения — абсолютные, в рублях
float_error_rub = abs(Decimal.from_float(balance_float) - exact)
decimal_error_rub = abs(balance_decimal - exact)

# Процент расхождения относительно точного результата
float_error_percent = float_error_rub / exact * 100
decimal_error_percent = decimal_error_rub / exact * 100

print(f"Операций: {operations:,}")
print(f"Точное значение:       {exact} руб.")
print(f"float:                 {balance_float:.12f} руб.")
print(f"Decimal:               {balance_decimal} руб.")
print(f"Целые копейки:         {balance_kopecks} коп. = {balance_int} руб.")
print()
print(f"Ошибка float:          {float_error_rub} руб.")
print(f"Ошибка float:          {float_error_percent:.12E}%")
print(f"Ошибка Decimal:        {decimal_error_rub} руб.")
print(f"Ошибка Decimal:        {decimal_error_percent:.12E}%")
print(f"Ошибка int-копеек:     {abs(balance_int - exact)} руб.")
