#include <iostream>

int main() {
    // Локализация для корректного вывода кириллицы
    std::setlocale(LC_ALL, "ru_RU.UTF-8");

    // Часть 1: int -> char (сужение)
    int big = 300;
    char small = big; // Неявное сужение: 300 не помещается в стандартный char

    std::cout << "=== Сужение int -> char ===\n";
    std::cout << "int big = " << big << "\n";
    
    // static_cast<int> нужен, чтобы вывести числовой код символа, а не сам символ
    std::cout << "char small (числовое значение): " << static_cast<int>(small) << "\n";
    std::cout << "char small (как символ): " << small << "\n";

    std::cout << "sizeof(int):   " << sizeof(int) << " байт\n";
    std::cout << "sizeof(char):  " << sizeof(char) << " байт\n\n";

    // Часть 2: double -> int (сужение)
    double d = 3.99;
    int i = d; // Неявное сужение: дробная часть просто отбрасывается

    std::cout << "=== Сужение double -> int ===\n";
    std::cout << "double d = " << d << "\n";
    std::cout << "int i = " << i << "\n";

    return 0;
}