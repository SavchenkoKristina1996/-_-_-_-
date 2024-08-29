from flask import Flask, request, render_template_string
import numpy as np
import joblib
import requests

app = Flask(__name__)

# Загрузка моделей
model_modulus = joblib.load('model_modulus.pkl')
model_strength = joblib.load('model_strength.pkl')

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Предсказание свойств материала</title>
    <style>
        body {
            background-color: #f0f8ff;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            color: #333;
        }
        form {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-top: 10px;
            color: #555;
        }
        input[type="text"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-top: 5px;
            border-radius: 5px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 15px 30px;
            margin-top: 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        h2 {
            color: #333;
        }
    </style>
</head>
<body>
    <form method="post">
        <h1>Предсказание свойств материала</h1>
        <label for="matrix_filler_ratio">Matrix Filler Ratio:</label>
        <input type="text" id="matrix_filler_ratio" name="matrix_filler_ratio" required>

        <label for="density_kg_m3">Density (kg/m³):</label>
        <input type="text" id="density_kg_m3" name="density_kg_m3" required>

        <label for="elastic_modulus_gpa">Elastic Modulus (GPa):</label>
        <input type="text" id="elastic_modulus_gpa" name="elastic_modulus_gpa" required>

        <label for="hardener_amount_percent">Hardener Amount (%):</label>
        <input type="text" id="hardener_amount_percent" name="hardener_amount_percent" required>

        <label for="epoxy_groups_content_percent">Epoxy Groups Content (%):</label>
        <input type="text" id="epoxy_groups_content_percent" name="epoxy_groups_content_percent" required>

        <label for="flash_point_temp_c">Flash Point Temp (°C):</label>
        <input type="text" id="flash_point_temp_c" name="flash_point_temp_c" required>

        <label for="surface_density_g_m2">Surface Density (g/m²):</label>
        <input type="text" id="surface_density_g_m2" name="surface_density_g_m2" required>

        <label for="resin_consumption_g_m2">Resin Consumption (g/m²):</label>
        <input type="text" id="resin_consumption_g_m2" name="resin_consumption_g_m2" required>

        <label for="stitching_angle_deg">Stitching Angle (°):</label>
        <input type="text" id="stitching_angle_deg" name="stitching_angle_deg" required>

        <label for="stitching_step">Stitching Step:</label>
        <input type="text" id="stitching_step" name="stitching_step" required>

        <label for="stitching_density">Stitching Density:</label>
        <input type="text" id="stitching_density" name="stitching_density" required>

        <input type="submit" value="Предсказать">

        {% if prediction_modulus is not none %}
        <h2>Предсказанный модуль упругости (GPa): {{ prediction_modulus }}</h2>
        {% endif %}        
        {% if prediction_strength is not none %}
        <h2>Предсказанная прочность (MPa): {{ prediction_strength }}</h2>
        {% endif %}
    </form>
</body>
</html>
"""

TELEGRAM_TOKEN = '7532434789:AAEI2Gu-0pLxNX2x-TLDFPXUQ350Vp50mbk'
TELEGRAM_CHAT_ID = '841934109'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction_modulus = None
    prediction_strength = None
    if request.method == 'POST':
        # Получаем данные из формы
        data = [
            float(request.form['matrix_filler_ratio']),
            float(request.form['density_kg_m3']),
            float(request.form['elastic_modulus_gpa']),
            float(request.form['hardener_amount_percent']),
            float(request.form['epoxy_groups_content_percent']),
            float(request.form['flash_point_temp_c']),
            float(request.form['surface_density_g_m2']),
            float(request.form['resin_consumption_g_m2']),
            float(request.form['stitching_angle_deg']),
            float(request.form['stitching_step']),
            float(request.form['stitching_density'])
        ]

        # Преобразуем данные в формат, подходящий для модели
        data = np.array(data).reshape(1, -1)

        # Делаем предсказания
        prediction_modulus = model_modulus.predict(data)[0]
        prediction_strength = model_strength.predict(data)[0]
        # Формируем сообщение для отправки в Telegram
        message = (
            f"Предсказание выполнено:\n"
            f"Модуль упругости (GPa): {prediction_modulus:.2f}\n"
            f"Прочность (MPa): {prediction_strength:.2f}"
        )

        # Отправляем сообщение в Telegram
        send_telegram_message(message)


    return render_template_string(html_template, prediction_modulus=prediction_modulus, prediction_strength=prediction_strength)

if __name__ == '__main__':
    app.run(debug=True)





