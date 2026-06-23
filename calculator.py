from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """<!doctype html>
<title>Calculator</title>
<form action='/calculate' method='post'>
  <input type='number' name='num1' step='any' required>
  <select name='op'>
    <option value='+'>+</option>
    <option value='-'>-</option>
    <option value='*'>*</option>
    <option value='/'>/</option>
  </select>
  <input type='number' name='num2' step='any' required>
  <button type='submit'>Calculate</button>
</form>
{% if result is not none %}<p>Result: {{ result }}</p>{% endif %}
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML, result=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        op = request.form['op']
    except (KeyError, ValueError):
        return render_template_string(HTML, result="Invalid input")

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        if num2 == 0:
            result = 'Error: Division by zero'
        else:
            result = num1 / num2
    else:
        result = f'Unknown operator: {op}'

    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True)
