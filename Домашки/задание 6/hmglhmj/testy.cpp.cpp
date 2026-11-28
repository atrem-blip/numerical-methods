#include <iostream>
#include <string>
#include <stdexcept> // Для std::invalid_argument и std::out_of_range

int main() {
    std::string input;

    // Часть 1: Работа с целым числом через std::stoi
    std::cout << "Введите целое число: ";
    std::getline(std::cin, input); // getline позволяет корректно считать строку целиком

    try {
        // std::stoi преобразует строку в int. 
        // Второй параметр (nullptr) указывает, что нам не нужно знать, 
        // на каком символе закончился разбор числа.
        int number = std::stoi(input);
        
        int multiplied = number * 3;

        // Вывод результата как числа
        std::cout << "Результат умножения на 3 (как число): " << multiplied << std::endl;

        // std::to_string преобразует число обратно в строку
        std::string result_str = std::to_string(multiplied);
        std::cout << "Результат умножения на 3 (как строка): " << result_str << std::endl;

    } catch (const std::invalid_argument& e) {
        std::cerr << "Ошибка: введенная строка не содержит числа." << std::endl;
        return 1;
    } catch (const std::out_of_range& e) {
        std::cerr << "Ошибка: число выходит за пределы диапазона типа int." << std::endl;
        return 1;
    }

    // Часть 2: Преобразование строки в double через std::stod
    std::string pi_str = "3.14";
    
    try {
        // std::stod преобразует строку в double
        double pi = std::stod(pi_str);
        
        std::cout << "\nПреобразование строки \"" << pi_str << "\" в double: " << pi << std::endl;

        // Демонстрация std::to_string для double
        std::string pi_back_to_str = std::to_string(pi);
        std::cout << "Обратное преобразование double в строку: " << pi_back_to_str << std::endl;

    } catch (const std::invalid_argument& e) {
        std::cerr << "Ошибка: строку невозможно преобразовать в double." << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Ошибка: число выходит за пределы диапазона типа double." << std::endl;
    }

    return 0;
}