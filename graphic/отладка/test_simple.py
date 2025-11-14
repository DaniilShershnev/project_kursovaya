import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.function_plotter import FunctionPlotter
import params_global


plotter = FunctionPlotter(vars(params_global))

plotter.add_curve_from_latex(
    formula_latex=r'\sinh(x)',
    params={},
    x_range=[0, 10],
    style={'linestyle': '-', 'color': 'blue', 'linewidth': 1.5}
)

plotter.set_axes(
    xlim=[0, 10],
    ylim=[0, 100],
    xlabel='x',
    ylabel='y'
)

output_path = os.path.join(os.path.dirname(__file__), 'output', 'test_simple3.svg')
plotter.save(output_path)

print(f"График создан: {output_path}")