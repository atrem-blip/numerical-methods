#include <iostream>
#include <iomanip> // Для std::boolalpha

int main() {
    // Целочисленные типы
    int age = 28;
    short temperature = -15;
    long long population = 1470000000LL; // Суффикс LL для long long
    unsigned int fileSize = 2147483648u; // Суффикс u для unsigned int

    // Вещественные типы
    float piApprox = 3.14159f; // Суффикс f для float
    double gravity = 9.80665;  // По умолчанию double

    // Символьный и логический типы
    char grade = 'A';
    bool isRegistered = true;

    // Вывод значений и размеров
    std::cout << "--- Целочисленные типы ---\n";
    std::cout << "int age: " << age << " (размер: " << sizeof(age) << " байт)\n";
    std::cout << "short temperature: " << temperature << " (размер: " << sizeof(temperature) << " байт)\n";
    std::cout << "long long population: " << population << " (размер: " << sizeof(population) << " байт)\n";
    std::cout << "unsigned int fileSize: " << fileSize << " (размер: " << sizeof(fileSize) << " байт)\n";

    std::cout << "\n--- Вещественные типы ---\n";
    std::cout << "float piApprox: " << piApprox << " (размер: " << sizeof(piApprox) << " байт)\n";
    std::cout << "double gravity: " << gravity << " (размер: " << sizeof(gravity) << " байт)\n";

    std::cout << "\n--- Символьный и логический типы ---\n";
    std::cout << "char grade: " << grade << " (размер: " << sizeof(grade) << " байт)\n";
    
    // std::boolalpha заставляет std::cout выводить true/false вместо 1/0
    std::cout << std::boolalpha;
    std::cout << "bool isRegistered: " << isRegistered << " (размер: " << sizeof(isRegistered) << " байт)\n";

    return 0;
}