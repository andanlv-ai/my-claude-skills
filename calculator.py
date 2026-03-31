"""
Calculator Module - Object-Oriented Approach
Использует класс с историей операций и расширяемую архитектуру
"""

from typing import List, Tuple
from datetime import datetime


class Calculator:
    """Калькулятор с историей операций"""
    
    def __init__(self):
        self.history: List[Tuple[str, float, float, float, datetime]] = []
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел"""
        result = a + b
        self._log_operation('add', a, b, result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание"""
        result = a - b
        self._log_operation('subtract', a, b, result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение"""
        result = a * b
        self._log_operation('multiply', a, b, result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Деление с проверкой на ноль"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        result = a / b
        self._log_operation('divide', a, b, result)
        return result
    
    def _log_operation(self, op: str, a: float, b: float, result: float):
        """Логирование операции в историю"""
        self.history.append((op, a, b, result, datetime.now()))
    
    def get_history(self) -> List[str]:
        """Получить историю операций"""
        return [
            f"{timestamp.strftime('%H:%M:%S')}: {a} {op} {b} = {result}"
            for op, a, b, result, timestamp in self.history
        ]
    
    def clear_history(self):
        """Очистить историю"""
        self.history.clear()


# Пример использования
if __name__ == "__main__":
    calc = Calculator()
    
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"5 - 3 = {calc.subtract(5, 3)}")
    print(f"5 * 3 = {calc.multiply(5, 3)}")
    print(f"5 / 3 = {calc.divide(5, 3):.2f}")
    
    print("\nИстория операций:")
    for entry in calc.get_history():
        print(f"  {entry}")
