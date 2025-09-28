# flask_full_calculator_app.py
# Красивый и интерактивный Flask калькулятор с улучшенным дизайном и анимациями на фронтенде.

from flask import Flask, request, render_template_string
import math, datetime

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Интерактивные калькуляторы</title>
  <style>
    body {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(to right, #f0f4f8, #d9e2ec); margin:0; padding:0;}
    header {background:#3f72af; color:white; padding:20px; text-align:center; box-shadow: 0 2px 5px rgba(0,0,0,0.2);}
    h1 {margin:0; font-size:2rem;}
    .container {max-width: 900px; margin:20px auto; padding:20px;}
    .card {background:white; border-radius:12px; padding:20px; margin-bottom:20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.3s;}
    .card:hover {transform: translateY(-5px);}
    input, select, button {padding:10px; margin:5px; border-radius:6px; border:1px solid #ccc; font-size:1rem;}
    button {background:#3f72af; color:white; border:none; cursor:pointer; transition: background 0.3s;}
    button:hover {background:#112d4e;}
    .result {margin-top:10px; font-weight:bold; font-size:1.2rem; color:#112d4e;}
    footer {text-align:center; padding:15px; color:#555; font-size:0.9rem;}
  </style>
  <script>
    function animateResult(id) {
      const el = document.getElementById(id);
      el.style.transform = 'scale(1.2)';
      setTimeout(() => el.style.transform = 'scale(1)', 300);
    }
  </script>
</head>
<body>
<header><h1>Интерактивные калькуляторы на Python</h1></header>
<div class="container">
  <div class="card">
    <h2>Базовый калькулятор</h2>
    <form method="post" action="/basic">
      <input name="a" type="number" step="any" placeholder="Число A" required>
      <select name="op">
        <option value="+">+</option>
        <option value="-">-</option>
        <option value="*">*</option>
        <option value="/">/</option>
        <option value="%">%</option>
        <option value="**">^</option>
      </select>
      <input name="b" type="number" step="any" placeholder="Число B" required>
      <button type="submit">Посчитать</button>
    </form>
    {% if basic is defined %}<div class="result" id="basicResult" onload="animateResult('basicResult')">{{basic}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>Научный калькулятор</h2>
    <form method="post" action="/scientific">
      <input name="expr" type="text" placeholder="Пример: sin(1)+log(10)" size="40" required>
      <button type="submit">Вычислить</button>
    </form>
    {% if scientific is defined %}<div class="result" id="sciResult">{{scientific}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>Конвертеры</h2>
    <form method="post" action="/convert">
      <select name="kind">
        <option value="temp">Температура (C↔F)</option>
        <option value="length">Длина (m↔ft)</option>
        <option value="weight">Вес (kg↔lb)</option>
      </select>
      <input name="value" type="number" step="any" placeholder="Значение" required>
      <select name="direction">
        <option value="forward">Основное → Вторичное</option>
        <option value="back">Вторичное → Основное</option>
      </select>
      <button type="submit">Конвертировать</button>
    </form>
    {% if convert is defined %}<div class="result" id="convResult">{{convert}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>Ипотечный калькулятор</h2>
    <form method="post" action="/mortgage">
      <input name="principal" type="number" step="any" placeholder="Сумма кредита" required>
      <input name="annual_rate" type="number" step="any" placeholder="Годовая ставка (%)" required>
      <input name="years" type="number" step="1" placeholder="Срок (лет)" required>
      <button type="submit">Рассчитать платёж</button>
    </form>
    {% if mortgage is defined %}<div class="result">Ежемесячный платёж: {{mortgage}} | Общая выплата: {{mortgage_total}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>BMI</h2>
    <form method="post" action="/bmi">
      <input name="weight" type="number" step="any" placeholder="Вес (кг)" required>
      <input name="height" type="number" step="any" placeholder="Рост (м)" required>
      <button type="submit">Рассчитать BMI</button>
    </form>
    {% if bmi is defined %}<div class="result">BMI: {{bmi}} — {{bmi_cat}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>Программистский калькулятор</h2>
    <form method="post" action="/prog">
      <input name="number" type="text" placeholder="Число" required>
      <select name="base">
        <option value="dec">10</option>
        <option value="hex">16</option>
        <option value="bin">2</option>
      </select>
      <button type="submit">Преобразовать</button>
    </form>
    {% if prog is defined %}<div class="result">{{prog}}</div>{% endif %}
  </div>

  <div class="card">
    <h2>Разница между датами</h2>
    <form method="post" action="/datediff">
      <input name="d1" type="date" required>
      <input name="d2" type="date" required>
      <button type="submit">Посчитать</button>
    </form>
    {% if datediff is defined %}<div class="result">Разница: {{datediff}}</div>{% endif %}
  </div>

</div>
<footer>Сделано на Python + Flask | Красивый и интерактивный интерфейс</footer>
</body>
</html>
'''

SAFE_NAMES = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
SAFE_NAMES.update({'abs': abs, 'round': round})

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

@app.route('/basic', methods=['POST'])
def basic_calc():
    a = request.form['a']
    b = request.form['b']
    op = request.form['op']
    try:
        x = float(a)
        y = float(b)
        res = {'+': x+y, '-': x-y, '*': x*y, '/': x/y if y!=0 else 'Ошибка деления', '%': x%y, '**': x**y}.get(op, 'Неизвестная операция')
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, basic=res)

@app.route('/scientific', methods=['POST'])
def scientific():
    expr = request.form['expr']
    try:
        code = compile(expr, '<string>', 'eval')
        for name in code.co_names:
            if name not in SAFE_NAMES:
                raise NameError(f'Недопустимое имя: {name}')
        res = eval(code, {'__builtins__': {}}, SAFE_NAMES)
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, scientific=res)

@app.route('/convert', methods=['POST'])
def convert():
    kind = request.form['kind']
    val = float(request.form['value'])
    direction = request.form['direction']
    try:
        if kind == 'temp': res = f"{val} °C = {(val*9/5)+32} °F" if direction=='forward' else f"{val} °F = {(val-32)*5/9} °C"
        elif kind == 'length': res = f"{val} m = {val*3.28084} ft" if direction=='forward' else f"{val} ft = {val/3.28084} m"
        elif kind == 'weight': res = f"{val} kg = {val*2.20462} lb" if direction=='forward' else f"{val} lb = {val/2.20462} kg"
        else: res='Неизвестный конвертер'
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, convert=res)

@app.route('/mortgage', methods=['POST'])
def mortgage():
    P = float(request.form['principal'])
    r = float(request.form['annual_rate'])/100/12
    n = int(request.form['years'])*12
    try:
        monthly = P/n if r==0 else P*(r*(1+r)**n)/((1+r)**n-1)
        total = monthly*n
        monthly, total = round(monthly,2), round(total,2)
    except Exception as e:
        monthly, total = f'Ошибка: {e}', ''
    return render_template_string(TEMPLATE, mortgage=monthly, mortgage_total=total)

@app.route('/bmi', methods=['POST'])
def bmi():
    w = float(request.form['weight'])
    h = float(request.form['height'])
    try:
        val = w/(h*h)
        cat = 'норма'
        if val<18.5: cat='недостаток веса'
        elif val<25: cat='норма'
        elif val<30: cat='излишний вес'
        else: cat='ожирение'
        res = round(val,2)
    except Exception as e:
        res, cat = f'Ошибка: {e}', ''
    return render_template_string(TEMPLATE, bmi=res, bmi_cat=cat)

@app.route('/prog', methods=['POST'])
def prog():
    num = request.form['number']
    base = request.form['base']
    try:
        n = int(num, {'dec':10,'hex':16,'bin':2}[base])
        res = f"dec: {n} | hex: {hex(n)} | bin: {bin(n)}"
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, prog=res)

@app.route('/datediff', methods=['POST'])
def datediff():
    d1 = request.form['d1']
    d2 = request.form['d2']
    try:
        diff = abs((datetime.date.fromisoformat(d2)-datetime.date.fromisoformat(d1)).days)
        res = f"{diff} дней"
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, datediff=res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)