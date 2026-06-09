import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_bih_weather(city: str) -> str:
    """"Fetches real time weather data for specified city in Bosnia and Herzegovina"""
    coordinates = {
        "sarajevo": {"lat": 43.8486, "lon": 18.3564},
        "mostar": {"lat": 43.3438, "lon": 17.8078},
        "banja luka": {"lat": 44.7722, "lon": 17.1910},
        "tuzla": {"lat": 44.5384, "lon": 18.6671},
        "zenica": {"lat": 44.2016, "lon": 17.9039}
    }

    city_clean = city.lower().strip()

    if city_clean not in coordinates:
        loc = coordinates["sarajevo"]
        city_name = "Sarajevo (Default)"
    else:
        loc = coordinates[city_clean]
        city_name = city.capitalize()
    url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,rain_sum&timezone=Europe/Berlin"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current_weather"]
        tomorrow_max = data["daily"]["temperature_2m_max"][1]
        tomorrow_min = data["daily"]["temperature_2m_min"][1]
        tomorrow_rain = data["daily"]["rain_sum"][1]

        weather_report = {
            "city": city_name,
            "current_temp": current['temperature'],
            "max_temp": tomorrow_max,
            "min_temp": tomorrow_min,
            "rain_mm": tomorrow_rain
        }
        return weather_report
    except Exception as e:
        return {}

def send_email(report_content: str, recipient_email: str):
    """Sends a report email"""
    smtp_server = "sandbox.smtp.mailtrap.io"
    smtp_port = 2525
    smtp_user = "1f413bb94e6c44"
    smtp_pass = "f561966c108f75"

    msg = MIMEMultipart()
    msg['From'] = "ai.weathert@multiai.com"
    msg['To'] = recipient_email
    msg['Subject'] = "Your Daily Weather and Outfit Recommendation"

    msg.attach(MIMEText(report_content, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            return "Email sent successfully"
    except Exception as e:
        return "Error sending email"