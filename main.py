import tools
import agents

def weather_styling_pipeline(target_city: str, email_destination: str):
    print(f"[Weather Agent] Fetching live weather data for {target_city}...")
    weather_info = tools.get_bih_weather(target_city)

    if not weather_info:
        print("[Weather Agent] Failed to retrieve weather data.")
        return

    print(f"[Weather Agent] Successfully gathered data for {weather_info['city']}.")
    print(f"[Weather Agent] Max Temp: {weather_info['max_temp']}°C, Rain: {weather_info['rain_mm']}mm\n")

    print("[Weather Agent] Activating Stylist Agent... ")
    stylist = agents.StyleAgent()
    raw_styling_report = stylist.analyze_and_style(weather_info)
    print("[Weather Agent] Styling recommendations successfully generated.\n")

    print("[Weather Agent] Activating Email Formatting Agent... ")
    writer = agents.EmailAgent()
    final_email = writer.format_email(raw_styling_report)
    print("[Weather Agent] Final email layout successfully generated.\n")

    print(f"[Weather Agent] Sending the final recommendation email to {email_destination}...")
    delivery_status = tools.send_email(final_email, email_destination)

    print(f"[Weather Agent] Pipeline execution finished. Status: {delivery_status}")


if __name__ == "__main__":
    CITY = "Tuzla"
    MY_EMAIL = "ernajaticc@gmail.com"

    weather_styling_pipeline(CITY, MY_EMAIL)
