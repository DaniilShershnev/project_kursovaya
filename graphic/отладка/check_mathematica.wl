(* Параметры из p28b.yaml и params_global.py *)
a = 0;
j = 2;
v = 1;
c = 0.3;
b = 1*10^(-12);
h = 0.07;

(* Уравнения системы *)
(* ds/dt = a * Exp[v * w] - s * Exp[(v - j) * w] *)
(* dw/dt = c * (1 - w - b * Exp[h * s] * (1 + w)) *)

(* Начальные условия для всех 5 кривых *)
initialConditions = {
  {100, 0.8},
  {200, 0.8},
  {300, 0.8},
  {400, 0.8},
  {500, 0.8}
};

(* Решаем систему ОДУ для каждого начального условия *)
solutions = Table[
  NDSolve[
    {
      s'[t] == a * Exp[v * w[t]] - s[t] * Exp[(v - j) * w[t]],
      w'[t] == c * (1 - w[t] - b * Exp[h * s[t]] * (1 + w[t])),
      s[0] == initialConditions[[i, 1]],
      w[0] == initialConditions[[i, 2]]
    },
    {s, w},
    {t, 0, 7}
  ],
  {i, 1, 5}
];

(* Извлекаем функции s[t] из решений *)
sFunctions = Table[s /. solutions[[i, 1]], {i, 1, 5}];

(* Цвета для графиков *)
colors = {Blue, Red, Green, Orange, Purple};

(* Строим график только s(t) для всех начальных условий *)
plot = Plot[
  Evaluate[Table[sFunctions[[i]][t], {i, 1, 5}]],
  {t, 0, 7},
  PlotRange -> {{0, 7}, {0, 500}},
  PlotStyle -> Table[{colors[[i]], Thick}, {i, 1, 5}],
  PlotLegends -> {
    "s0=100, w0=0.8",
    "s0=200, w0=0.8",
    "s0=300, w0=0.8",
    "s0=400, w0=0.8",
    "s0=500, w0=0.8"
  },
  AxesLabel -> {"t", "s"},
  PlotLabel -> "Графики s(t) для разных начальных условий",
  GridLines -> Automatic,
  ImageSize -> Large
]

(* Проверка производных в начальной точке *)
Print["=== Проверка производных в t=0 ==="];
Do[
  s0 = initialConditions[[i, 1]];
  w0 = initialConditions[[i, 2]];
  dsdt0 = a * Exp[v * w0] - s0 * Exp[(v - j) * w0];
  dwdt0 = c * (1 - w0 - b * Exp[h * s0] * (1 + w0));
  bExpTerm = b * Exp[h * s0];
  Print["s0=", s0, ", w0=", w0];
  Print["  ds/dt(0) = ", N[dsdt0, 6]];
  Print["  dw/dt(0) = ", N[dwdt0, 6]];
  Print["  b*Exp[h*s0] = ", N[bExpTerm, 6]];
  Print[""];
, {i, 1, 5}];

(* Проверка пересечений в конкретные моменты времени *)
Print["=== Проверка пересечений ==="];
checkTimes = {0.5, 1.0, 2.0, 3.0, 5.0, 7.0};
Do[
  Print["В момент времени t=", tCheck];
  values = Table[sFunctions[[i]][tCheck], {i, 1, 5}];
  Do[
    Print["  s0=", initialConditions[[i, 1]], ": s(t)=", N[values[[i]], 6]];
  , {i, 1, 5}];

  (* Проверяем монотонность *)
  isMonotonic = And @@ Table[values[[i]] > values[[i+1]], {i, 1, 4}];
  Print["  Порядок сохранен (s500 > s400 > s300 > s200 > s100)? ", isMonotonic];
  If[!isMonotonic, Print["  *** КРИВЫЕ ПЕРЕСЕКЛИСЬ! ***"]];
  Print[""];
, {tCheck, checkTimes}];

(* Экспортируем график *)
Export["D:\\graphic\\mathematica_check.png", plot, ImageResolution -> 150];
Print["График сохранен в D:\\graphic\\mathematica_check.png"];
