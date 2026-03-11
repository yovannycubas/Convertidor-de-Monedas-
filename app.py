import os
from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

FRANKFURTER_API_URL = "https://api.frankfurter.app"

def get_currencies():
    try:
        response = requests.get(f"{FRANKFURTER_API_URL}/currencies")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching currencies: {e}")
        return {}

def get_latest_rate(from_curr, to_curr, amount=1):
    try:
        response = requests.get(f"{FRANKFURTER_API_URL}/latest", params={
            "amount": amount,
            "from": from_curr,
            "to": to_curr
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching latest rate: {e}")
        return None

def get_historical_data(from_curr, to_curr):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    try:
        response = requests.get(f"{FRANKFURTER_API_URL}/{start_date}..{end_date}", params={
            "from": from_curr,
            "to": to_curr
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None

def generate_chart(data, from_curr, to_curr):
    rates = data.get('rates', {})
    dates = sorted(rates.keys())
    values = [rates[date][to_curr] for date in dates]
    
    if not values:
        return None

    plt.figure(figsize=(10, 5))
    plt.style.use('dark_background')
    
    plt.plot(dates, values, marker='o', linestyle='-', color='#00d4ff', linewidth=2, markersize=4)
    
    # Mark min and max
    min_val = min(values)
    max_val = max(values)
    min_idx = values.index(min_val)
    max_idx = values.index(max_val)
    
    plt.scatter(dates[min_idx], min_val, color='red', s=100, label=f'Mín: {min_val:.4f}', zorder=5)
    plt.scatter(dates[max_idx], max_val, color='green', s=100, label=f'Máx: {max_val:.4f}', zorder=5)
    
    plt.title(f'Historial 30 días: {from_curr} a {to_curr}', fontsize=14, pad=20)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Tasa de cambio', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    currencies = get_currencies()
    if not currencies:
        return render_template('error.html', message="No se pudo conectar con la API de Frankfurter.")

    if request.method == 'POST':
        try:
            from_curr = request.form.get('from_curr')
            to_curr = request.form.get('to_curr')
            amount = float(request.form.get('amount', 1))

            # Swap logic (handled by frontend, but valid here too)
            if 'swap' in request.form:
                from_curr, to_curr = to_curr, from_curr

            latest = get_latest_rate(from_curr, to_curr, amount)
            if not latest:
                raise Exception("Error al obtener la tasa actual.")

            unit_rate = get_latest_rate(from_curr, to_curr, 1)
            
            historical = get_historical_data(from_curr, to_curr)
            chart_url = None
            if historical:
                chart_url = generate_chart(historical, from_curr, to_curr)

            return render_template('index.html', 
                                 currencies=currencies,
                                 result=latest['rates'][to_curr],
                                 unit_rate=unit_rate['rates'][to_curr],
                                 date=latest['date'],
                                 from_curr=from_curr,
                                 to_curr=to_curr,
                                 amount=amount,
                                 chart_url=chart_url)
        except Exception as e:
            return render_template('error.html', message=str(e))

    return render_template('index.html', currencies=currencies, from_curr='EUR', to_curr='USD', amount=1)

@app.errorhandler(500)
@app.errorhandler(404)
def handle_error(e):
    return render_template('error.html', message="Ha ocurrido un error inesperado."), 500

if __name__ == '__main__':
    app.run(debug=True)
