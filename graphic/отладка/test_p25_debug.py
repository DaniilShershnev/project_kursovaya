import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sympy.parsing.latex import parse_latex
import sympy as sp

print("=== ТЕСТ ПАРСИНГА УРАВНЕНИЙ ===\n")

# Неправильное уравнение из p25.yaml
wrong_eq = "c * (1 - w(1+b*\\exp(h * s))"
print(f"Неправильное: {wrong_eq}")
try:
    parsed_wrong = parse_latex(wrong_eq)
    print(f"Распарсилось как: {parsed_wrong}")
    print(f"Свободные символы: {parsed_wrong.free_symbols}")
except Exception as e:
    print(f"Ошибка парсинга: {e}")

print("\n" + "="*50 + "\n")

# Правильное уравнение
correct_eq = "c * (1 - w - b * \\exp(h * s) * (1 + w))"
print(f"Правильное: {correct_eq}")
try:
    parsed_correct = parse_latex(correct_eq)
    print(f"Распарсилось как: {parsed_correct}")
    print(f"Свободные символы: {parsed_correct.free_symbols}")
except Exception as e:
    print(f"Ошибка парсинга: {e}")

print("\n" + "="*50 + "\n")

# Проверим производную для конкретных значений
print("=== СРАВНЕНИЕ ЗНАЧЕНИЙ ===")
s_val, w_val = 400, 0.02
c_val, b_val, h_val = 0.3, 1e-12, 0.07

print(f"При s={s_val}, w={w_val}, c={c_val}, b={b_val}, h={h_val}:\n")

# Правильная формула
import numpy as np
dwdt_correct = c_val * (1 - w_val - b_val * np.exp(h_val * s_val) * (1 + w_val))
print(f"Правильная формула: dw/dt = {dwdt_correct:.6f}")

# Попробуем понять, что считает неправильная
# w(...) интерпретируется как функция, это даст ошибку при вычислении
print("\nНеправильная формула не может быть вычислена, т.к. w(...) это функция, а не переменная")
