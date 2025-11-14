import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.ode_system import ODESystem
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

# Уравнения
equations_latex = ["a * \\exp(\\betta * w) - s * \\exp((\\betta - \\alpha) * w)",
                   "c * (1 - w * (1 + b * \\exp(h * s)))"]
variable_names = ['s', 'w']

system = ODESystem(equations_latex, variable_names)

params = {
    'a': 0,
    'alpha': 2,
    'betta': 1,
    'c': 0.3,
    'b': 1.0e-12,
    'h': 0.07
}

param_values = [params[str(p)] for p in system.params]

# Решаем для одного случая
initial_conditions = [400, 0.8]
t_span = [0, 8]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

sol = solve_ivp(
    lambda t, y: system.right_hand_side(t, y, param_values),
    t_span,
    initial_conditions,
    method='DOP853',
    t_eval=t_eval
)

# Создаем график с двумя осями
fig, ax1 = plt.subplots(figsize=(8, 8))

# Левая ось для s
ax1.plot(sol.t, sol.y[0], 'b-', linewidth=2, label='s(t)')
ax1.set_xlabel('t')
ax1.set_ylabel('s', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_ylim([0, 500])
ax1.set_xlim([0, 8])

# Правая ось для w
ax2 = ax1.twinx()
ax2.plot(sol.t, sol.y[1], 'r--', linewidth=2, label='w(t)')
ax2.set_ylabel('w', color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim([0, 1])

plt.title('Проверка двойной оси: s (синий, левая ось) и w (красный, правая ось)')
fig.tight_layout()
plt.savefig('D:\\graphic\\test_dual_axis_check.png', dpi=150)
print("Тестовый график сохранен в D:\\graphic\\test_dual_axis_check.png")
plt.close()

print(f"\nПроверка значений:")
print(f"s(0) = {sol.y[0][0]:.2f}, должно быть ~400")
print(f"s(8) = {sol.y[0][-1]:.2f}, должно быть близко к 0")
print(f"w(0) = {sol.y[1][0]:.4f}, должно быть 0.8")
print(f"w(8) = {sol.y[1][-1]:.4f}, должно быть близко к 1")
print(f"\nДиапазон s: [{sol.y[0].min():.2f}, {sol.y[0].max():.2f}] - должен быть в [0, 500]")
print(f"Диапазон w: [{sol.y[1].min():.4f}, {sol.y[1].max():.4f}] - должен быть в [0, 1]")
