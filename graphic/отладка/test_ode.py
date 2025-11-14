import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ode_plotter import ODEPlotter
import params_global


# Тест 1: Временные зависимости
plotter1 = ODEPlotter(vars(params_global))

#Тут много разных примеров, которые я тестировал. Они все работают корректно, их все все можно раскоментить и они будут работать.

#Простая система: dx/dt = y, dy/dt = -x
# equations = [r'y', r'-x']
# variable_names = ['x', 'y']
# initial_conditions = [1.0, 0.0]
#--------------Второй пример--------------
# equations = [r'y', r'-0.5 \cdot y - x']
# variable_names = ['x', 'y']
# initial_conditions = [2.0, 0.0]
# t_span = [0, 15]
#---------Третий пример--------------------
# equations = [r'x - x \cdot y', r'-y + x \cdot y']
# variable_names = ['x', 'y']
# initial_conditions = [1.5, 1.0]
# t_span = [0, 20]

#Уравнения можно записывать в привычном латех коде, все автоматически компилируется благодаря библиотеке

equations = [r'-s \cdot \exp(-w)',r'c \cdot (1 - w - b \cdot \exp(h \cdot s) \cdot (1 + w))']

variable_names = ['s', 'w']

initial_conditions = [400, 0.02]  # s₀=100, w₀=0.02  указываем начальные параметры, на самом деле они уже указаны в глобальных параметрах
#ок

params = {
    'c': 0.3,
    'b': 1e-12,
    'h': 0.07
}

t_span = [0, 100]  # это наше время


plotter1.solve_and_plot_time(
    equations_latex=equations,
    variable_names=variable_names,
    initial_conditions=initial_conditions,
    params=params,
    t_span=t_span,
    style_list=[
        {'linestyle': '-', 'color': 'blue', 'linewidth': 1.5, 'label': 's(t)'},
        {'linestyle': '--', 'color': 'red', 'linewidth': 1.5, 'label': 'w(t)'}
    ]
)

plotter1.set_axes(
    xlim=[0,6],
    ylim=[0,500],
    xlabel='t',
    ylabel='значение'
)

plotter1.ax.legend()

output_path1 = os.path.join(os.path.dirname(__file__), 'output', 'test_ode_time2.svg')
plotter1.save(output_path1)

print(f"График временных зависимостей создан: {output_path1}")


# Тест 2: Фазовый портрет

plotter2 = ODEPlotter(vars(params_global))

plotter2.solve_and_plot_phase(
    equations_latex=equations,
    variable_names=variable_names,
    initial_conditions=initial_conditions,
    params=params,
    t_span=t_span,
    var_indices=[0, 1],
    style={'linestyle': '-', 'color': 'green', 'linewidth': 1.5}
)

plotter2.set_axes(
    xlim=[0,500],
    ylim=None,
    xlabel='s',
    ylabel='w', 
    #equal_aspect=True
)
output_path2 = os.path.join(os.path.dirname(__file__), 'output', 'test_ode_phase2.svg')
plotter2.save(output_path2)

print(f"Фазовый портрет создан: {output_path2}")