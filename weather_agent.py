import requests
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.tools import tool
import os

# Load environment variables from .env file
load_dotenv()

# --------------------------- Weather Tool -----------------
@tool                                     
def get_weather(city: str) -> str:
    """
    Returns current weather of a city
    """
    print(f"Fetching weather for ahmedabad:")
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()
    temp = data["current_condition"][0]["temp_C"]
    return f"Temperature in {city} is {temp} C"

# --------------------------- OpenAI Client -----------------
client = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

client_with_tools = client.bind_tools([get_weather])

response = client_with_tools.invoke("what is the weather in Ahmedabad")

print(response.tool_calls)

if response.tool_calls:
    tool_call = response.tool_calls[0]   
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name == "":
         result = get_weather.invoke(tool_args)
         print(result)

    result = get_weather.invoke(tool_args)

    print(result)
else:
    print(response.content)


