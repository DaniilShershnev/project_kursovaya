"""
Вычисление положения равновесия и других характеристик
для степенной модели тиксотропных сред

Модель:
- G(w) = G₀·w^α
- η(w) = η₀·w^β
- ṡ = a·w^β - s·w^(β-α)
- ẇ = c[(1-w) - bg(s)w]

Положение равновесия:
- s* = a·(w*)^α
- w* = 1/(1 + bg(s*))
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, brentq
import os

# Материальные функции
def g_exp(s, h):
    """Экспоненциальная МФ: g(s) = e^(hs)"""
    return np.exp(h * s)

def g_quadratic(s, h):
    """Квадратичная МФ: g(s) = 1 + (hs)²"""
    return 1 + (h * s)**2

def g_linear(s, h):
    """Линейная МФ: g(s) = 1 + hs"""
    return 1 + h * s

# Словарь МФ
MATERIAL_FUNCTIONS = {
    'exp': g_exp,
    'quadratic': g_quadratic,
    'linear': g_linear
}

def equilibrium_equations(s, a, b, alpha, h, g_func):
    """
    Уравнение для нахождения равновесного напряжения s*
    Из системы:
    - s* = a·(w*)^α
    - w* = 1/(1 + bg(s*))

    Подставляя второе в первое:
    ln(s*/a) = α·ln(w*) = -α·ln(1 + bg(s*))
    или
    s*/a = [1/(1 + bg(s*))]^α
    """
    w_star = 1.0 / (1.0 + b * g_func(s, h))
    s_calc = a * (w_star ** alpha)
    return s_calc - s

def find_equilibrium(a, b, alpha, h, g_type='exp'):
    """
    Находит положение равновесия (s*, w*) для заданных параметров
    """
    g_func = MATERIAL_FUNCTIONS[g_type]

    # Начальное приближение
    s0 = a

    try:
        # Решаем уравнение относительно s*
        s_star = fsolve(lambda s: equilibrium_equations(s, a, b, alpha, h, g_func), s0)[0]

        # Вычисляем w*
        w_star = 1.0 / (1.0 + b * g_func(s_star, h))

        return s_star, w_star
    except:
        return None, None

def compute_discriminant(s_star, w_star, a, b, alpha, beta, c, h, g_type='exp'):
    """
    Вычисляет дискриминант характеристического уравнения
    D = [cw* - e^(-(α-β)w*)]² - 4abc·w*·g'(s*)·e^(βw*)
    """
    g_func = MATERIAL_FUNCTIONS[g_type]

    # Производная g'(s*) численно
    ds = 0.001
    g_prime = (g_func(s_star + ds, h) - g_func(s_star - ds, h)) / (2 * ds)

    # Формула для степенной модели требует адаптации
    # Из DOCX: D = [cw* - e^(-(α-β)w*)]² - 4ce^(-(α-β)w*)·w*·abc·w*·g'(s*)·e^(βw*)
    term1 = c * w_star - (w_star ** (-(alpha - beta)))
    term2 = 4 * c * (w_star ** (-(alpha - beta))) * w_star * a * b * c * (w_star ** beta) * w_star * g_prime

    D = term1**2 - term2
    return D

def plot_s_w_vs_parameter(param_values, param_name, a_fixed=1, b_fixed=0.01, alpha_fixed=2,
                          beta_fixed=1, c_fixed=0.3, h=0.1, g_types=['exp', 'quadratic', 'linear'],
                          output_dir='output/power_law'):
    """
    Строит зависимости s*(param) и w*(param)
    """
    colors = ['black', 'blue', 'red']
    linestyles = ['-', '--', ':']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for idx, g_type in enumerate(g_types):
        s_values = []
        w_values = []

        for param in param_values:
            # Устанавливаем параметры
            if param_name == 'b':
                a, b, alpha, beta = a_fixed, param, alpha_fixed, beta_fixed
            elif param_name == 'alpha':
                a, b, alpha, beta = a_fixed, b_fixed, param, beta_fixed
            elif param_name == 'a':
                a, b, alpha, beta = param, b_fixed, alpha_fixed, beta_fixed
            else:
                raise ValueError(f"Unknown parameter: {param_name}")

            s_star, w_star = find_equilibrium(a, b, alpha, h, g_type)
            if s_star is not None:
                s_values.append(s_star)
                w_values.append(w_star)
            else:
                s_values.append(np.nan)
                w_values.append(np.nan)

        # График s*(param)
        ax1.plot(param_values, s_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

        # График w*(param)
        ax2.plot(param_values, w_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

    ax1.set_xlabel(param_name)
    ax1.set_ylabel('s*')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_xlabel(param_name)
    ax2.set_ylabel('w*')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # Сохранение
    os.makedirs(output_dir, exist_ok=True)
    filename = f'fig_s_w_vs_{param_name}_power.svg'
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

    print(f"Saved: {filename}")

def plot_apparent_viscosity_vs_parameter(param_values, param_name, a_fixed=1, b_fixed=0.01,
                                          alpha_fixed=2, beta_fixed=1, c_fixed=0.3, h=0.1,
                                          g_types=['exp', 'quadratic', 'linear'],
                                          output_dir='output/power_law'):
    """
    Строит зависимость кажущейся вязкости μ(a)/η₀ = (w*)^β от параметра
    """
    colors = ['black', 'blue', 'red']
    linestyles = ['-', '--', ':']

    fig, ax = plt.subplots(figsize=(8, 6))

    for idx, g_type in enumerate(g_types):
        viscosity_values = []

        for param in param_values:
            # Устанавливаем параметры
            if param_name == 'b':
                a, b, alpha, beta = a_fixed, param, alpha_fixed, beta_fixed
            elif param_name == 'alpha':
                a, b, alpha, beta = a_fixed, b_fixed, param, beta_fixed
            elif param_name == 'a':
                a, b, alpha, beta = param, b_fixed, alpha_fixed, beta_fixed
            else:
                raise ValueError(f"Unknown parameter: {param_name}")

            s_star, w_star = find_equilibrium(a, b, alpha, h, g_type)
            if s_star is not None and w_star is not None:
                # Кажущаяся вязкость: μ(a)/η₀ = (w*)^β
                mu_app = w_star ** beta
                viscosity_values.append(mu_app)
            else:
                viscosity_values.append(np.nan)

        # График μ(a)/η₀ vs param
        ax.plot(param_values, viscosity_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

    ax.set_xlabel(param_name)
    ax.set_ylabel('μ(a)/η₀')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Сохранение
    os.makedirs(output_dir, exist_ok=True)
    filename = f'fig5_viscosity_vs_{param_name}_power.svg'
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

    print(f"Saved: {filename}")

def plot_phase_space_curves(a_fixed=1, b_fixed=0.01, alpha_fixed=2, beta_fixed=1,
                             c_fixed=0.3, h=0.1, g_types=['exp', 'quadratic', 'linear'],
                             output_dir='output/power_law'):
    """
    Строит кривые в фазовом пространстве (s, w):
    - Параметрическая кривая {s*(b), w*(b)}
    - Параметрическая кривая {s*(α), w*(α)}
    """
    colors = ['black', 'blue', 'red']
    linestyles = ['-', '--', ':']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Левый график: кривые {s*(b), w*(b)}
    b_values = np.logspace(-3, 0, 100)
    for idx, g_type in enumerate(g_types):
        s_values = []
        w_values = []

        for b in b_values:
            s_star, w_star = find_equilibrium(a_fixed, b, alpha_fixed, h, g_type)
            if s_star is not None:
                s_values.append(s_star)
                w_values.append(w_star)
            else:
                s_values.append(np.nan)
                w_values.append(np.nan)

        ax1.plot(s_values, w_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

    ax1.set_xlabel('s*')
    ax1.set_ylabel('w*')
    ax1.set_title('Кривые {s*(b), w*(b)}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Правый график: кривые {s*(α), w*(α)}
    alpha_values = np.linspace(0.1, 10, 100)
    for idx, g_type in enumerate(g_types):
        s_values = []
        w_values = []

        for alpha in alpha_values:
            s_star, w_star = find_equilibrium(a_fixed, b_fixed, alpha, h, g_type)
            if s_star is not None:
                s_values.append(s_star)
                w_values.append(w_star)
            else:
                s_values.append(np.nan)
                w_values.append(np.nan)

        ax2.plot(s_values, w_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

    ax2.set_xlabel('s*')
    ax2.set_ylabel('w*')
    ax2.set_title('Кривые {s*(α), w*(α)}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # Сохранение
    os.makedirs(output_dir, exist_ok=True)
    filename = 'fig3_phase_space_curves_power.svg'
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

    print(f"Saved: {filename}")

def plot_discriminant_vs_parameter(param_values, param_name, a_fixed=1, b_fixed=0.01,
                                    alpha_fixed=2, beta_fixed=1, c_fixed=0.3, h=0.1,
                                    g_types=['exp'], output_dir='output/power_law'):
    """
    Строит зависимость дискриминанта D от параметра
    """
    colors = ['black', 'blue', 'red']
    linestyles = ['-', '--', ':']

    fig, ax = plt.subplots(figsize=(8, 6))

    for idx, g_type in enumerate(g_types):
        D_values = []

        for param in param_values:
            # Устанавливаем параметры
            if param_name == 'a':
                a, b, alpha, beta, c = param, b_fixed, alpha_fixed, beta_fixed, c_fixed
            elif param_name == 'b':
                a, b, alpha, beta, c = a_fixed, param, alpha_fixed, beta_fixed, c_fixed
            elif param_name == 'c':
                a, b, alpha, beta, c = a_fixed, b_fixed, alpha_fixed, beta_fixed, param
            else:
                raise ValueError(f"Unknown parameter: {param_name}")

            # Находим равновесие
            s_star, w_star = find_equilibrium(a, b, alpha, h, g_type)

            if s_star is not None and w_star is not None:
                # Вычисляем дискриминант
                D = compute_discriminant(s_star, w_star, a, b, alpha, beta, c, h, g_type)
                D_values.append(D)
            else:
                D_values.append(np.nan)

        # График D vs param
        ax.plot(param_values, D_values, color=colors[idx], linestyle=linestyles[idx],
                linewidth=1.5, label=f'g={g_type}')

    # Линия D=0 (граница между узлом и фокусом)
    ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xlabel(param_name)
    ax.set_ylabel('D')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Сохранение
    os.makedirs(output_dir, exist_ok=True)
    filename = f'fig_discriminant_vs_{param_name}_power.svg'
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

    print(f"Saved: {filename}")

# Основная программа
if __name__ == "__main__":
    print("Вычисление характеристик степенной модели...")

    # Создание директории для выходных файлов
    output_dir = 'output/power_law'
    os.makedirs(output_dir, exist_ok=True)

    # Параметры по умолчанию
    h = 0.1

    # Рис. 1: s*(b) и w*(b)
    print("\nРис. 1: Зависимости s*(b) и w*(b)")
    b_values = np.logspace(-3, 0, 100)  # от 0.001 до 1
    plot_s_w_vs_parameter(b_values, 'b', a_fixed=1, alpha_fixed=2, h=h, output_dir=output_dir)

    # Рис. 2: s*(α) и w*(α)
    print("\nРис. 2: Зависимости s*(α) и w*(α)")
    alpha_values = np.linspace(0.1, 10, 100)
    plot_s_w_vs_parameter(alpha_values, 'alpha', a_fixed=1, b_fixed=0.01, h=h, output_dir=output_dir)

    # Рис. 4: s*(a) и w*(a)
    print("\nРис. 4: Зависимости s*(a) и w*(a)")
    a_values = np.linspace(0.1, 50, 100)
    plot_s_w_vs_parameter(a_values, 'a', b_fixed=0.01, alpha_fixed=2, h=h, output_dir=output_dir)

    # Рис. 5: μ(a)/η₀ vs a
    print("\nРис. 5: Зависимость кажущейся вязкости μ(a)/η₀ от a")
    a_values = np.linspace(0.1, 50, 100)
    plot_apparent_viscosity_vs_parameter(a_values, 'a', b_fixed=0.01, alpha_fixed=2, h=h, output_dir=output_dir)

    # Рис. 3: Кривые в фазовом пространстве
    print("\nРис. 3: Кривые в фазовом пространстве {s*(b), w*(b)} и {s*(α), w*(α)}")
    plot_phase_space_curves(a_fixed=1, b_fixed=0.01, alpha_fixed=2, h=h, output_dir=output_dir)

    # Рис. 6: Дискриминант D(a)
    print("\nРис. 6: Зависимость дискриминанта D от a")
    a_values = np.linspace(0.1, 50, 100)
    plot_discriminant_vs_parameter(a_values, 'a', b_fixed=0.01, alpha_fixed=2, c_fixed=0.3, h=h,
                                    g_types=['exp'], output_dir=output_dir)

    # Рис. 7: Дискриминант D(c)
    print("\nРис. 7: Зависимость дискриминанта D от c")
    c_values = np.linspace(0.01, 1, 100)
    plot_discriminant_vs_parameter(c_values, 'c', a_fixed=1, b_fixed=0.01, alpha_fixed=2, h=h,
                                    g_types=['exp'], output_dir=output_dir)

    # Рис. 8: Дискриминант D(b)
    print("\nРис. 8: Зависимость дискриминанта D от b")
    b_values = np.logspace(-3, 0, 100)
    plot_discriminant_vs_parameter(b_values, 'b', a_fixed=1, alpha_fixed=2, c_fixed=0.3, h=h,
                                    g_types=['exp'], output_dir=output_dir)

    print("\nГотово! Графики сохранены в:", output_dir)
