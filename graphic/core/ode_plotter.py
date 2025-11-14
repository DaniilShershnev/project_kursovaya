from core.base_plotter import GraphPlotter
from models.ode_system import ODESystem
from utils.validators import merge_params
from scipy.integrate import solve_ivp
import numpy as np


class ODEPlotter(GraphPlotter):
    def __init__(self, global_params):
        super().__init__()
        self.global_params = global_params

    def solve_and_plot_time(self, equations_latex, variable_names, initial_conditions, params, t_span, style_list, solver_method=None):
        system = ODESystem(equations_latex, variable_names)

        merged_params = merge_params(self.global_params, params)

        param_values = [merged_params[str(p)] for p in system.params]

        t_span_use = merged_params.get('t_span', t_span)
        rtol = merged_params.get('rtol', 1e-9)
        atol = merged_params.get('atol', 1e-12)
        n_points = merged_params.get('n_points', 1000)
        method = solver_method or merged_params.get('default_solver_method', 'DOP853')

        t_eval = np.linspace(t_span_use[0], t_span_use[1], n_points)

        sol = solve_ivp(
            lambda t, y: system.right_hand_side(t, y, param_values),
            t_span_use,
            initial_conditions,
            method=method,
            rtol=rtol,
            atol=atol,
            t_eval=t_eval
        )

        for i, style in enumerate(style_list):
            # Проверяем, нужно ли рисовать на правой оси
            if isinstance(style, dict):
                use_right_axis = style.get('use_right_axis', False)
                # Создаем копию стиля без параметра use_right_axis (он не нужен для plot)
                plot_style = {k: v for k, v in style.items() if k != 'use_right_axis'}
            else:
                use_right_axis = False
                plot_style = style
            self.add_curve(sol.t, sol.y[i], plot_style, use_right_axis=use_right_axis)

    def solve_and_plot_phase(self, equations_latex, variable_names, initial_conditions, params, t_span, var_indices,
                             style, solver_method=None):
        system = ODESystem(equations_latex, variable_names)

        merged_params = merge_params(self.global_params, params)

        param_values = [merged_params[str(p)] for p in system.params]

        t_span_use = merged_params.get('t_span', t_span)
        rtol = merged_params.get('rtol', 1e-9)
        atol = merged_params.get('atol', 1e-12)
        n_points = merged_params.get('n_points', 1000)
        method = solver_method or merged_params.get('default_solver_method', 'DOP853')

        t_eval = np.linspace(t_span_use[0], t_span_use[1], n_points)

        sol = solve_ivp(
            lambda t, y: system.right_hand_side(t, y, param_values),
            t_span_use,
            initial_conditions,
            method=method,
            rtol=rtol,
            atol=atol,
            t_eval=t_eval
        )

        x_var = sol.y[var_indices[0]]
        y_var = sol.y[var_indices[1]]

        self.add_curve(x_var, y_var, style)

    def add_vector_field(self, equations_latex, variable_names, params, var_indices, field_config):
        from models.ode_system import ODESystem
        import numpy as np

        system = ODESystem(equations_latex, variable_names)

        merged_params = merge_params(self.global_params, params)
        param_values = [merged_params[str(p)] for p in system.params]

        # Получить пределы осей
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Создать сетку точек
        density = field_config.get('density', 20)
        x_grid = np.linspace(xlim[0], xlim[1], density)
        y_grid = np.linspace(ylim[0], ylim[1], density)
        X, Y = np.meshgrid(x_grid, y_grid)

        # Вычислить векторы направлений
        U = np.zeros_like(X)
        V = np.zeros_like(Y)

        for i in range(density):
            for j in range(density):
                state = [0] * len(variable_names)
                state[var_indices[0]] = X[i, j]
                state[var_indices[1]] = Y[i, j]

                derivatives = system.right_hand_side(0, state, param_values)
                U[i, j] = derivatives[var_indices[0]]
                V[i, j] = derivatives[var_indices[1]]

        # Простая нормализация - все стрелки одинаковой длины
        magnitude = np.sqrt(U ** 2 + V ** 2)
        magnitude[magnitude == 0] = 1  # избежать деления на 0
        U_norm = U / magnitude
        V_norm = V / magnitude

        # Построить векторное поле
        self.ax.quiver(
            X, Y, U_norm, V_norm,
            color=field_config.get('color', 'pink'),
            alpha=field_config.get('alpha', 0.3),
            scale=field_config.get('scale', 30),
            width=field_config.get('width', 0.003),
            headwidth=3,
            headlength=4
        )