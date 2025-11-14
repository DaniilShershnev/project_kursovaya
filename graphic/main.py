import sys
import os
import argparse  #библиотека для парсинга командной строки

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config_loader import load_config
from utils.validators import validate_config
from core.function_plotter import FunctionPlotter
from core.ode_plotter import ODEPlotter
import params_global

#Функция ниже определяет типа графика и проверяет корректность типа графика, после чего вызывает либо соответствующий обработчик графика либо выкидывает ошибку Unkown type.
def plot_from_config(config):
    validate_config(config) # проверяет корректность входных данных config, в случае ошибки выбрасывает через raise ошибку и останавливает программу.

    plot_type = config['type']  # извлекаем из словаря config тип графика

    if plot_type == 'function':
        plot_function(config)
    elif plot_type == 'ode_time':
        plot_ode_time(config)
    elif plot_type == 'phase_portrait':
        plot_phase_portrait(config)
    else:
        raise ValueError(f"Unknown type: {plot_type}")


def plot_function(config):
    plotter = FunctionPlotter(vars(params_global))

    for curve in config['curves']:
        plotter.add_curve_from_latex(
            formula_latex=curve['formula'],      #тип str
            params=curve.get('params', {}),      #словарь, хранит параметры
            x_range=curve['x_range'],            #список, хранить пределы x
            style=curve['style']                 #словарь, хранит информацию о стилях
        )

    axes = config.get('axes', {})                #словарь, или {}
    plotter.set_axes(
        xlim=axes.get('xlim'),                   #[x_min, x_max] или None
        ylim=axes.get('ylim'),                   #[y_min, y_max] или None
        xlabel=axes.get('xlabel', ''),           #str, по умолчанию ''
        ylabel=axes.get('ylabel', ''),           #str, по умолчанию ''
        grid=axes.get('grid', False),            #bool, по умолчанию False, то есть нет сетки по дефолту
        equal_aspect=axes.get('equal_aspect', False), #
        spines=axes.get('spines'),
        grid_style=axes.get('grid_style'),
        axis_labels_at_end=axes.get('axis_labels_at_end', False)
    )

    #if any('label' in curve['style'] for curve in config['curves']):
    #    plotter.ax.legend()

    output_path = os.path.join('output', config['output']) # делаем правильное объединение путей, чтобы у Гоши работало тоже.
    plotter.save(output_path)                              # сохраняем график в формате SVG
    print(f"График создан: {output_path}")


def plot_ode_time(config):
    plotter = ODEPlotter(vars(params_global))

    # ВАЖНО: Если используется dual_y_axis, создаем вторую ось ДО добавления кривых
    axes = config.get('axes', {})
    if axes.get('dual_y_axis', False):
        plotter.enable_dual_y_axis()

    for curve in config['curves']:
        plotter.solve_and_plot_time(
            equations_latex=curve['equations'],
            variable_names=curve['variable_names'],
            initial_conditions=curve['initial_conditions'],
            params=curve.get('params', {}),
            t_span=curve['t_span'],
            style_list=curve['styles'],
            solver_method=curve.get('solver_method')
        )

    plotter.set_axes(
        xlim=axes.get('xlim'),
        ylim=axes.get('ylim'),
        xlabel=axes.get('xlabel', ''),
        ylabel=axes.get('ylabel', ''),
        grid=axes.get('grid', True),
        equal_aspect=axes.get('equal_aspect', False),
        spines=axes.get('spines'),
        grid_style=axes.get('grid_style'),
        axis_labels_at_end=axes.get('axis_labels_at_end', False),
        dual_y_axis=axes.get('dual_y_axis', False),
        ylim_right=axes.get('ylim_right'),
        ylabel_right=axes.get('ylabel_right', ''),
        yticks_right=axes.get('yticks_right')
    )

    #

    output_path = os.path.join('output', config['output'])
    plotter.save(output_path)
    print(f"График создан: {output_path}")


def plot_phase_portrait(config):
    plotter = ODEPlotter(vars(params_global))

    # Сначала установить пределы осей
    axes = config.get('axes', {})
    if axes.get('xlim') and axes.get('ylim'):
        plotter.ax.set_xlim(axes['xlim'])
        plotter.ax.set_ylim(axes['ylim'])

    # Затем построить векторное поле (если есть)
    vector_field = config.get('vector_field')
    if vector_field and vector_field.get('enabled', False):
        first_curve = config['curves'][0]
        plotter.add_vector_field(
            equations_latex=first_curve['equations'],
            variable_names=first_curve['variable_names'],
            params=first_curve.get('params', {}),
            var_indices=first_curve['var_indices'],
            field_config=vector_field
        )

    # Построить траектории
    for curve in config['curves']:
        plotter.solve_and_plot_phase(
            equations_latex=curve['equations'],
            variable_names=curve['variable_names'],
            initial_conditions=curve['initial_conditions'],
            params=curve.get('params', {}),
            t_span=curve['t_span'],
            var_indices=curve['var_indices'],
            style=curve['style'],
            solver_method=curve.get('solver_method')
        )

    plotter.set_axes(
        xlim=axes.get('xlim'),
        ylim=axes.get('ylim'),
        xlabel=axes.get('xlabel', ''),
        ylabel=axes.get('ylabel', ''),
        grid=axes.get('grid', True),
        equal_aspect=axes.get('equal_aspect', False),
        spines=axes.get('spines'),
        grid_style=axes.get('grid_style'),
        xticks=axes.get('xticks'),
        yticks=axes.get('yticks'),
        axis_labels_at_end=axes.get('axis_labels_at_end', False)
    )

    output_path = os.path.join('output', config['output'])
    plotter.save(output_path)
    print(f"График создан: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Построение графиков из YAML конфигурации')
    parser.add_argument('--config', required=True, help='Путь к YAML файлу конфигурации')

    args = parser.parse_args()

    config = load_config(args.config)
    plot_from_config(config)