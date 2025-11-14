import matplotlib.pyplot as plt  # как будет видно ниже, очень удобно использовать сокращение переменных.
import numpy as np               # тоже сократим для красоты


# На всякий случай комментарий:
# перед переменными мы пишем self. так как мы ссылаемся на объект класса. В C++ указателем на объект класса было this->
# Espessialy for Gosha: в питоне нет строго разделения переменных на приватные и публичные

#GraphPlotter - это базовый класс, от которого наследуется(пока что) два класса: FunctionPlotter и ODEPlotter
class GraphPlotter:
    # Ниже def __init__(self): - это конструктор, им инициализируем переменные по умолчанию. В функции __init__ пишем self, self является указателем на создаваемый объект.
    def __init__(self):
        plt.rcParams['font.family'] = 'Times New Roman'    #указываем нужный шрифт. Для теста можно указать Impact, будет заметен результат сразу.
        plt.rcParams['font.size'] = 14                     #указываем нужный размер шриафта.
        #Можно указывать разный размер текста для разных элементов:
        plt.rcParams['axes.labelsize'] = 14                #размер подписей осей
        plt.rcParams['xtick.labelsize'] = 14               #разметка по оси ox
        plt.rcParams['ytick.labelsize'] = 14               #разметка по оси oy
        plt.rcParams['legend.fontsize'] = 14               #легенда
        self.fig, self.ax = plt.subplots(figsize=(8,8))   # соотношение сторон, по факту растяжение
        self.ax2 = None  # Вторая ось Y (правая), создается при необходимости
        self.curves = []

    def enable_dual_y_axis(self):
        """Создает вторую ось Y (правую) для отображения данных в другом масштабе"""
        if self.ax2 is None:
            self.ax2 = self.ax.twinx()
        return self.ax2

    def set_axes(self, xlim=None, ylim=None, xlabel='', ylabel='', grid=False, equal_aspect=False, spines=None,
                 grid_style=None, xticks=None, yticks=None, axis_labels_at_end=False,
                 dual_y_axis=False, ylim_right=None, ylabel_right='', yticks_right=None):
        # Создаем вторую ось, если требуется
        if dual_y_axis and self.ax2 is None:
            self.enable_dual_y_axis()

        # Настройка левой оси Y
        if xlim:
            self.ax.set_xlim(xlim)
        if ylim:
            self.ax.set_ylim(ylim)

        # Настройка правой оси Y
        if self.ax2 is not None and ylim_right:
            self.ax2.set_ylim(ylim_right)

        # Если нужно разместить подписи у концов осей
        if axis_labels_at_end:
            # Убираем стандартные подписи
            self.ax.set_xlabel('')
            self.ax.set_ylabel('')

            # Получаем пределы осей
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()

            # Подпись оси X (справа от конца оси)
            if xlabel:
                self.ax.text(x_max, y_min, f' {xlabel}',
                           ha='left', va='top', fontsize=14)

            # Подпись оси Y (сверху от конца оси)
            if ylabel:
                self.ax.text(x_min, y_max, f' {ylabel}',
                           ha='left', va='bottom', fontsize=14)
        else:
            # Стандартные подписи по центру
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)

            # Подпись правой оси Y
            if self.ax2 is not None and ylabel_right:
                self.ax2.set_ylabel(ylabel_right)

        # Настройка делений осей
        if xticks:
            self.ax.set_xticks(xticks)
        if yticks:
            self.ax.set_yticks(yticks)
        if self.ax2 is not None and yticks_right:
            self.ax2.set_yticks(yticks_right)

        # Настройка границ (spines)
        if spines:
            for spine in ['top', 'right', 'bottom', 'left']:
                if spine in spines:
                    self.ax.spines[spine].set_visible(spines[spine])

        # Настройка сетки
        if grid:
            if grid_style:
                self.ax.grid(True, **grid_style)
            else:
                self.ax.grid(True, alpha=0.3)
        else:
            self.ax.grid(False)

        if equal_aspect:
            self.ax.set_aspect('equal')

    def add_curve(self, x, y, style, use_right_axis=False):
        """
        Добавляет кривую на график

        Параметры:
        - x, y: данные для построения
        - style: стиль линии (словарь с параметрами plot)
        - use_right_axis: если True, рисует на правой оси Y (требует dual_y_axis=True)
        """
        if use_right_axis and self.ax2 is not None:
            line, = self.ax2.plot(x, y, **style)
        else:
            line, = self.ax.plot(x, y, **style)
        self.curves.append(line)

    def save(self, filename):
        # Определяем формат по расширению файла
        import os
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.png':
            # Для PNG используем высокое разрешение (dpi=300)
            self.fig.savefig(filename, format='png', dpi=300, bbox_inches='tight')
        else:
            # По умолчанию SVG
            self.fig.savefig(filename, format='svg', bbox_inches='tight')

        plt.close(self.fig)
        #поямнения к формуле выше:


        # Чтобы сохранять абсолютно все точки, которые считаются(о чем речь - см файл), нужно:
        #import matplotlib as mpl
        #mpl.rcParams['path.simplify'] = False  # <-- Отключить упрощение
        #mpl.rcParams['path.simplify_threshold'] = 0.0  # <-- Порог = 0

        #self.fig.savefig(filename, format='svg', bbox_inches='tight')
        #plt.close(self.fig)

    def clear(self):
        self.ax.clear()
        self.curves = []