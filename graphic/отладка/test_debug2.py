import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.ode_system import ODESystem
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

# Уравнения из p28b.yaml
equations_latex = ["a * \\exp(v * w) - s * \\exp((v - j) * w)",
                   "c * (1 - w - b * \\exp(h * s) * (1 + w))"]
variable_names = ['s', 'w']

# Создаем систему
system = ODESystem(equations_latex, variable_names)

# Параметры
params = {
    'a': 0,
    'j': 2,
    'v': 1,
    'c': 0.3,
    'b': 1.0e-12,
    'h': 0.07
}

param_values = [params[str(p)] for p in system.params]

# Тестируем ВСЕ начальные условия из p28b.yaml
initial_conditions_list = [
    [100, 0.8],
    [200, 0.8],
    [300, 0.8],
    [400, 0.8],
    [500, 0.8]
]

t_span = [0, 7]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

print("=== ПРОВЕРКА ВСЕХ КРИВЫХ ===\n")

solutions = []
for ic in initial_conditions_list:
    sol = solve_ivp(
        lambda t, y: system.right_hand_side(t, y, param_values),
        t_span,
        ic,
        method='DOP853',
        t_eval=t_eval
    )
    solutions.append(sol)

    # Проверяем начальные производные
    derivs_0 = system.right_hand_side(0, ic, param_values)
    print(f"s0={ic[0]}, w0={ic[1]}:")
    print(f"  ds/dt(0) = {derivs_0[0]:.6f}")
    print(f"  dw/dt(0) = {derivs_0[1]:.9f}")

    # Проверяем член b * exp(h * s)
    b_exp_term = params['b'] * np.exp(params['h'] * ic[0])
    print(f"  b * exp(h * s0) = {b_exp_term:.6e}")
    print()

print("\n=== ПРОВЕРКА ПЕРЕСЕЧЕНИЙ ===\n")

# Построим график только для s(t)
plt.figure(figsize=(10, 6))
colors = ['blue', 'red', 'green', 'orange', 'purple']
for i, (sol, color) in enumerate(zip(solutions, colors)):
    s_values = sol.y[0]  # Только s
    plt.plot(sol.t, s_values, color=color, label=f's0={initial_conditions_list[i][0]}', linewidth=2)

plt.xlabel('t')
plt.ylabel('s')
plt.xlim(0, 7)
plt.ylim(0, 500)
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Графики s(t) для разных начальных условий')
plt.savefig('D:\\graphic\\debug_plot.png', dpi=150)
print("График сохранен в D:\\graphic\\debug_plot.png")
plt.close()

# Проверим, пересекаются ли кривые
print("\n=== ПРОВЕРКА ПЕРЕСЕЧЕНИЙ В ЗНАЧЕНИЯХ ===")
for t_idx in [100, 200, 500, 700, 900]:
    t = t_eval[t_idx]
    print(f"\nВ момент времени t={t:.3f}:")
    values = []
    for i, sol in enumerate(solutions):
        s_val = sol.y[0][t_idx]
        values.append(s_val)
        print(f"  s0={initial_conditions_list[i][0]}: s(t)={s_val:.4f}")

    # Проверяем монотонность
    is_monotonic = all(values[i] > values[i+1] for i in range(len(values)-1))
    print(f"  Порядок сохранен (s₅₀₀ > s₄₀₀ > s₃₀₀ > s₂₀₀ > s₁₀₀)? {is_monotonic}")
    if not is_monotonic:
        print("  *** ОШИБКА: КРИВЫЕ ПЕРЕСЕКЛИСЬ! ***")
