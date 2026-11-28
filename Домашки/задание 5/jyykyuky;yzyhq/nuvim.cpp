#include <iostream>
#include <iomanip> // Для std::setprecision
#include <limits>  // Для std::numeric_limits

int main() {
    int a, b;

    std::cout << "Введите два целых числа (a и b): ";
    if (!(std::cin >> a >> b)) {
        std::cerr << "Ошибка: введены некорректные данные." << std::endl;
        return 1;
    }

    // Проверка на деление на ноль
    if (b == 0) {
        std::cerr << "Ошибка: деление на ноль невозможно." << std::endl;
        return 1;
    }

    // 1. Целочисленное деление
    int int_div = a / b;
    std::cout << "Результат целочисленного деления (a / b): " << int_div << std::endl;

    // 2. Точный результат через static_cast
    // static_cast преобразует операнд 'a' из типа int в тип double. 
    // Поскольку один из операндов становится double, компилятор выполняет 
    // неявное приведение второго операнда (b) к double и деление с плавающей точкой.
    double float_div = static_cast<double>(a) / b;
    
    // Выводим с высокой точностью, чтобы увидеть все знаки после запятой
    std::cout << "Результат через static_cast<double>(a) / b: " 
              << std::setprecision(std::numeric_limits<double>::max_digits10) 
              << float_div << std::endl;

    // 3. Сравнение результатов
    std::cout << "\nСравнение:" << std::endl;
    if (int_div == float_div) {
        std::cout << "Результаты совпадают. Это происходит, когда число a делится на b без остатка." << std::endl;
    } else {
        std::cout << "Результаты различаются." << std::endl;
        std::cout << "Разница (float_div - int_div): " 
                  << std::setprecision(std::numeric_limits<double>::max_digits10) 
                  << (float_div - int_div) << std::endl;
    }

    return 0;
}