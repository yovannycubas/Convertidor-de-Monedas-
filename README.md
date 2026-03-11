# Convertidor de Divisas Premium

Una aplicación web moderna construida con **Flask** que permite convertir divisas en tiempo real utilizando la API pública de **Frankfurter** (datos del Banco Central Europeo).

## Características

- 📈 **Gráficos en Tiempo Real**: Visualización de la tendencia de los últimos 30 días mediante `matplotlib`.
- 🔴🟢 **Indicadores de Extremos**: Marcado automático de valores mínimos y máximos en el gráfico.
- 🔄 **Intercambio Rápido**: Botón para alternar instantáneamente entre la divisa de origen y destino.
- 🎨 **Interfaz Premium**: Diseño elegante con modo oscuro, efectos de desenfoque (glassmorphism) y totalmente responsivo.
- 🛠️ **Sin Necesidad de API Key**: Utiliza la API de Frankfurter, que es abierta y gratuita.

## Requisitos

- Python 3.x
- Flask
- Requests
- Matplotlib

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/convertidor.git
   cd convertidor
   ```

2. Instala las dependencias:
   ```bash
   pip install flask requests matplotlib
   ```

3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

4. Abre tu navegador en `http://127.0.0.1:5000`.

## Uso

1. Ingresa la cantidad a convertir.
2. Selecciona la divisa de origen y la de destino.
3. Haz clic en **Convertir Ahora**.
4. Desplázate hacia abajo para ver el gráfico histórico de los últimos 30 días.

## Créditos

Datos proporcionados por el [Banco Central Europeo](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) a través de la API [Frankfurter](https://www.frankfurter.app/).

---
Desarrollado con ❤️ usando Flask.
