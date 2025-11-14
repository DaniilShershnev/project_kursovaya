import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.ode_system import ODESystem
from scipy.integrate import solve_ivp
import numpy as np

# Уравнения из p28b.yaml
equations_latex = ["a * \\exp(v * w) - s * \\exp((v - j) * w)",
                   "c * (1 - w - b * \\exp(h * s) * (1 + w))"]
variable_names = ['s', 'w']

# Создаем систему
system = ODESystem(equations_latex, variable_names)

print("=== ДИАГНОСТИКА ===")
print(f"Уравнения LaTeX: {equations_latex}")
print(f"Переменные: {variable_names}")
print(f"Parsed equations: {system.equations}")
print(f"Parameters найденные в уравнениях: {[str(p) for p in system.params]}")
print()

# Параметры из params_global.py
params = {
    'a': 0,
    'j': 2,
    'v': 1,
    'c': 0.3,
    'b': 1.0e-12,
    'h': 0.07
}

# Получаем значения параметров в правильном порядке
param_values = [params[str(p)] for p in system.params]
print(f"Значения параметров (в порядке system.params): {param_values}")
print()

# Тестируем две начальные условия
initial_conditions_list = [
    ([100, 0.8], "s0=100"),
    ([200, 0.8], "s0=200")
]

t_span = [0, 7]
t_eval = np.linspace(t_span[0], t_span[1], 100)

for ic, label in initial_conditions_list:
    print(f"\n=== Тест для {label}, w0=0.8 ===")
    print(f"Начальные условия: s0={ic[0]}, w0={ic[1]}")

    # Решаем
    sol = solve_ivp(
        lambda t, y: system.right_hand_side(t, y, param_values),
        t_span,
        ic,
        method='DOP853',
        t_eval=t_eval
    )

    if sol.success:
        print(f"Решение найдено успешно")
        print(f"Первые 5 значений t: {sol.t[:5]}")
        print(f"Первые 5 значений s: {sol.y[0][:5]}")
        print(f"Первые 5 значений w: {sol.y[0][:5]}")
        print(f"Последние 5 значений s: {sol.y[0][-5:]}")
        print(f"Последние 5 значений w: {sol.y[1][-5:]}")

        # Проверяем производные в начальной точке
        derivs_0 = system.right_hand_side(0, ic, param_values)
        print(f"Производные в t=0: ds/dt={derivs_0[0]:.6f}, dw/dt={derivs_0[1]:.6f}")

        # Проверяем производные в середине
        t_mid = sol.t[50]
        y_mid = sol.y[:, 50]
        derivs_mid = system.right_hand_side(t_mid, y_mid, param_values)
        print(f"В t={t_mid:.2f}: s={y_mid[0]:.2f}, w={y_mid[1]:.6f}")
        print(f"Производные: ds/dt={derivs_mid[0]:.6f}, dw/dt={derivs_mid[1]:.6f}")
    else:
        print(f"ОШИБКА: {sol.message}")

print("\n=== Проверка формул вручную ===")
# Проверим формулы вручную для s0=100, w0=0.8
s, w = 100, 0.8
a, v, j, c, b, h = 0, 1, 2, 0.3, 1e-12, 0.07

dsdt = a * np.exp(v * w) - s * np.exp((v - j) * w)
dwdt = c * (1 - w - b * np.exp(h * s) * (1 + w))

print(f"Для s={s}, w={w}:")
print(f"  a * exp(v * w) = {a * np.exp(v * w):.6f}")
print(f"  s * exp((v - j) * w) = {s * np.exp((v - j) * w):.6f}")
print(f"  ds/dt = {dsdt:.6f}")
print(f"  b * exp(h * s) = {b * np.exp(h * s):.6e}")
print(f"  b * exp(h * s) * (1 + w) = {b * np.exp(h * s) * (1 + w):.6e}")
print(f"  dw/dt = {dwdt:.6f}")
