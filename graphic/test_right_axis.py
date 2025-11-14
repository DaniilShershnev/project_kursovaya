import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config_loader import load_config

config = load_config('configs/graphic_with_power_.yaml')

print("=== ПРОВЕРКА КОНФИГУРАЦИИ ===\n")
print(f"dual_y_axis: {config['axes'].get('dual_y_axis')}")
print(f"ylim_right: {config['axes'].get('ylim_right')}")
print(f"right spine: {config['axes']['spines'].get('right')}")

print("\n=== ПРОВЕРКА use_right_axis В СТИЛЯХ ===\n")
for i, curve in enumerate(config['curves']):
    print(f"Кривая {i+1}:")
    for j, style in enumerate(curve['styles']):
        has_right = style.get('use_right_axis', False)
        print(f"  Стиль {j+1}: color={style['color']}, linestyle={style['linestyle']}, use_right_axis={has_right}")

print("\n=== НАЧАЛЬНЫЕ УСЛОВИЯ ===\n")
for i, curve in enumerate(config['curves']):
    ic = curve['initial_conditions']
    print(f"Кривая {i+1}: s₀={ic[0]}, w₀={ic[1]}")
