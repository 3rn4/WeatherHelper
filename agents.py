import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HF_TOKEN')

llm_endpoint = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    task="text-generation",
    temperature=0.4,
    max_new_tokens=1024
)

llm = ChatHuggingFace(llm=llm_endpoint)

class StyleAgent():
    def __init__(self):
        self.system_message = SystemMessage(
            content= "You are an expert AI Fashion Stylist and Weather Consultant. Your job is to look at "
                    "weather data (temperatures, rain) and decide what clothing, footwear, and accessories "
                    "(like an umbrella, sunglasses, or a hat) a person should wear or carry."
        )

    def analyze_and_style(self, weather_data: dict) -> str:
        prompt = f"""
        Analyze this weather data for tomorrow:
        City: {weather_data.get('city')}
        Max Temperature: {weather_data.get('max_temp')}°C
        Min Temperature: {weather_data.get('min_temp')}°C
        Expected Rain: {weather_data.get('rain_mm')} mm
        
        Based on this, suggest a complete outfit (top, bottom, shoes) and explicitly state if they need 
        an umbrella, sunglasses, heavy jacket, or hat. Explain why.
        """

        response = llm.invoke([self.system_message, HumanMessage(content=prompt)])
        return response.content

class EmailAgent():
    def __init__(self):
        self.system_message = SystemMessage(
            content = "You are a polite Personal AI Assistant. Your job is to take a raw fashion/weather report "
                    "and format it into a beautiful, friendly, and structured daily email newsletter."
        )

    def format_email(self, raw_report: str) -> str:
        prompt = f"""
                Convert this raw recommendation report into a warm, friendly email for the user. 
                Start with 'Hi! Here is your personal weather and outfit recommendation for tomorrow...' 
                Use bullet points to make it easy to read.

                Raw Report:\n\n{raw_report}
                """
        response = llm.invoke([self.system_message, HumanMessage(content=prompt)])
        return response.content