def validate_config(config):
    required_keys = ['type', 'curves', 'output']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    if config['type'] not in ['function', 'ode_time', 'phase_portrait']:
        raise ValueError(f"Invalid type: {config['type']}")

    plot_type = config['type']

    # Список допустимых методов решения ОДУ
    valid_solver_methods = ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']

    for curve in config['curves']:
        if plot_type == 'function':
            if 'formula' not in curve:
                raise ValueError("Each function curve must have 'formula'")
            if 'x_range' not in curve:
                raise ValueError("Each function curve must have 'x_range'")
            if 'style' not in curve:
                raise ValueError("Each function curve must have 'style'")

        elif plot_type in ['ode_time', 'phase_portrait']:
            if 'equations' not in curve:
                raise ValueError("Each ODE curve must have 'equations'")
            if 'variable_names' not in curve:
                raise ValueError("Each ODE curve must have 'variable_names'")
            if 'initial_conditions' not in curve:
                raise ValueError("Each ODE curve must have 'initial_conditions'")
            if 't_span' not in curve:
                raise ValueError("Each ODE curve must have 't_span'")

            # Проверка метода решения ОДУ, если указан
            if 'solver_method' in curve:
                if curve['solver_method'] not in valid_solver_methods:
                    raise ValueError(f"Invalid solver_method: {curve['solver_method']}. Valid methods: {valid_solver_methods}")
 
    return True


def merge_params(global_params, local_params):
    merged = global_params.copy()
    if local_params:
        merged.update(local_params)
    return merged