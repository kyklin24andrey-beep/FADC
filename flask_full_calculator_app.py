# flask_full_calculator_app.py
# Single-file Flask app that implements many calculators (basic, scientific, programmer, unit conversions,
# mortgage, BMI, date difference) and serves a simple HTML UI. Includes a placeholder for Google AdSense script.
# Usage:
# 1. python -m venv env
# 2. source env/bin/activate   (or env\Scripts\activate on Windows)
# 3. pip install -r requirements.txt  (requirements: Flask)
# 4. python flask_full_calculator_app.py

from flask import Flask, request, render_template_string, redirect, url_for
import math, datetime

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Все калькуляторы на Python</title>
  <!-- TODO: вставьте сюда ваш Google AdSense код после одобрения -->
  <!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" crossorigin="anonymous"></script>
  <script>
    (adsbygoogle = window.adsbygoogle || []).push({});
  </script> -->
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Arial;margin:18px}
    .card{border:1px solid #ddd;border-radius:8px;padding:12px;margin-bottom:12px}
    input,select{padding:6px;margin:4px}
    .row{display:flex;gap:12px;flex-wrap:wrap}
  </style>
</head>
<body>
  <h1>Все калькуляторы — единый сайт</h1>
  <p>Пример: базовый, научный, конвертеры, ипотека, BMI, программистский, разница дат.</p>

  <div class="card">
    <h2>Базовый калькулятор</h2>
    <form method="post" action="/basic">
      <input name="a" type="text" placeholder="число A" required>
      <select name="op">
        <option value="+">+</option>
        <option value="-">-</option>
        <option value="*">*</option>
        <option value="/">/</option>
        <option value="%">%</option>
        <option value="**">^</option>
      </select>
      <input name="b" type="text" placeholder="число B" required>
      <button type="submit">Посчитать</button>
    </form>
    {% if basic is defined %}
      <p>Результат: <strong>{{basic}}</strong></p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Научный калькулятор</h2>
    <form method="post" action="/scientific">
      <input name="expr" type="text" placeholder="пример: sin(1)+log(10)" size="40" required>
      <button type="submit">Вычислить</button>
    </form>
    {% if scientific is defined %}
      <p>Результат: <strong>{{scientific}}</strong></p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Конвертеры (длина, вес, температура)</h2>
    <form method="post" action="/convert">
      <select name="kind">
        <option value="temp">Температура (C↔F)</option>
        <option value="length">Длина (m↔ft)</option>
        <option value="weight">Вес (kg↔lb)</option>
      </select>
      <input name="value" type="number" step="any" placeholder="значение" required>
      <select name="direction">
        <option value="forward">primary → secondary</option>
        <option value="back">secondary → primary</option>
      </select>
      <button type="submit">Конвертировать</button>
    </form>
    {% if convert is defined %}
      <p>Результат: <strong>{{convert}}</strong></p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Ипотечный калькулятор</h2>
    <form method="post" action="/mortgage">
      <input name="principal" type="number" step="any" placeholder="Сумма кредита" required>
      <input name="annual_rate" type="number" step="any" placeholder="Годовая ставка (%)" required>
      <input name="years" type="number" step="1" placeholder="Срок (лет)" required>
      <button type="submit">Рассчитать платёж</button>
    </form>
    {% if mortgage is defined %}
      <p>Ежемесячный платёж: <strong>{{mortgage}}</strong></p>
      <p>Общая выплата: <strong>{{mortgage_total}}</strong></p>
    {% endif %}
  </div>

  <div class="card">
    <h2>BMI</h2>
    <form method="post" action="/bmi">
      <input name="weight" type="number" step="any" placeholder="вес кг" required>
      <input name="height" type="number" step="any" placeholder="рост м" required>
      <button type="submit">Рассчитать BMI</button>
    </form>
    {% if bmi is defined %}
      <p>BMI: <strong>{{bmi}}</strong> — {{bmi_cat}}</p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Программистский калькулятор (decimal ↔ hex/bin)</h2>
    <form method="post" action="/prog">
      <input name="number" type="text" placeholder="число" required>
      <select name="base">
        <option value="dec">10</option>
        <option value="hex">16</option>
        <option value="bin">2</option>
      </select>
      <button type="submit">Преобразовать</button>
    </form>
    {% if prog is defined %}
      <p>Результат: <strong>{{prog}}</strong></p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Разница между датами</h2>
    <form method="post" action="/datediff">
      <input name="d1" type="date" required>
      <input name="d2" type="date" required>
      <button type="submit">Посчитать</button>
    </form>
    {% if datediff is defined %}
      <p>Разница: <strong>{{datediff}}</strong></p>
    {% endif %}
  </div>

  <footer style="margin-top:24px">Сделано на Python + Flask. Инструкции по хостингу и добавлению рекламы — в описании проекта.</footer>
</body>
</html>
'''

# Helper safety: limit eval for scientific expressions
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
        if op == '+': res = x + y
        elif op == '-': res = x - y
        elif op == '*': res = x * y
        elif op == '/': res = x / y if y != 0 else 'Ошибка: деление на 0'
        elif op == '%': res = x % y
        elif op == '**': res = x ** y
        else: res = 'Неизвестная операция'
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, basic=res)

@app.route('/scientific', methods=['POST'])
def scientific():
    expr = request.form['expr']
    # Разрешаем только имена из SAFE_NAMES и числа
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
        if kind == 'temp':
            if direction == 'forward': res = f"{val} °C = {(val*9/5)+32} °F"
            else: res = f"{val} °F = {(val-32)*5/9} °C"
        elif kind == 'length':
            if direction == 'forward': res = f"{val} m = {val*3.28084} ft"
            else: res = f"{val} ft = {val/3.28084} m"
        elif kind == 'weight':
            if direction == 'forward': res = f"{val} kg = {val*2.20462} lb"
            else: res = f"{val} lb = {val/2.20462} kg"
        else:
            res = 'Неизвестный конвертер'
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, convert=res)

@app.route('/mortgage', methods=['POST'])
def mortgage():
    P = float(request.form['principal'])
    r = float(request.form['annual_rate'])/100/12
    n = int(request.form['years'])*12
    try:
        if r == 0:
            monthly = P/n
        else:
            monthly = P * (r * (1+r)**n) / ((1+r)**n - 1)
        total = monthly * n
        monthly = round(monthly,2)
        total = round(total,2)
    except Exception as e:
        monthly = f'Ошибка: {e}'
        total = ''
    return render_template_string(TEMPLATE, mortgage=monthly, mortgage_total=total)

@app.route('/bmi', methods=['POST'])
def bmi():
    w = float(request.form['weight'])
    h = float(request.form['height'])
    try:
        val = w / (h*h)
        cat = 'норма'
        if val < 18.5: cat = 'недостаток веса'
        elif val < 25: cat = 'норма'
        elif val < 30: cat = 'излишний вес'
        else: cat = 'ожирение'
        res = round(val,2)
    except Exception as e:
        res = f'Ошибка: {e}'
        cat = ''
    return render_template_string(TEMPLATE, bmi=res, bmi_cat=cat)

@app.route('/prog', methods=['POST'])
def prog():
    num = request.form['number']
    base = request.form['base']
    try:
        if base == 'dec':
            n = int(num,10)
        elif base == 'hex':
            n = int(num,16)
        elif base == 'bin':
            n = int(num,2)
        else:
            return render_template_string(TEMPLATE, prog='неизвестная система')
        res = f"dec: {n} | hex: {hex(n)} | bin: {bin(n)}"
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, prog=res)

@app.route('/datediff', methods=['POST'])
def datediff():
    d1 = request.form['d1']
    d2 = request.form['d2']
    try:
        dt1 = datetime.date.fromisoformat(d1)
        dt2 = datetime.date.fromisoformat(d2)
        diff = abs((dt2 - dt1).days)
        res = f"{diff} дней"
    except Exception as e:
        res = f'Ошибка: {e}'
    return render_template_string(TEMPLATE, datediff=res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
