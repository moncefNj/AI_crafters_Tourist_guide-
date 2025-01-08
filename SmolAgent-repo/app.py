from smolagents.agents import ToolCallingAgent
from smolagents import tool, LiteLLMModel
from typing import Optional
import requests
import http.client
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurations
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")  # Default to GPT-4
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # GPT API Key
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # RapidAPI Key for football data

# Free API URLs
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
DUCKDUCKGO_URL = "https://api.duckduckgo.com/"

# System Message
SYSTEM_MESSAGE = (
    "You are an AI assistant that provides information on general searches, "
    "football matches, events, and trending news. Always ensure your responses are accurate "
    "and helpful. Use the provided tools to fetch real-time data and give the shortest response possible."
)

# Initialize the LiteLLMModel with GPT
model = LiteLLMModel(
    model_id=GPT_MODEL,
    api_key=OPENAI_API_KEY
)

# Define tools for the agent
@tool
def get_weather(location: str) -> str:
    """
    Get real-time weather information for the given location using a free Weather API.

    Args:
        location: The location for which the weather should be fetched.
    """
    api_key = os.getenv("FREE_WEATHER_API")
    if not api_key:
        return "Weather API key is missing. Please add it to the .env file."

    params = {
        "key": api_key,
        "q": location,
        "aqi": "no",
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        location_name = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        return f"The current weather in {location_name} is {temp_c}°C with {condition}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError:
        return "No weather data found. Please check the location and try again."


@tool
def get_match_event(event_id: str) -> str:
    """
    Fetch football match event details using RapidAPI.

    Args:
        event_id: The ID of the football match event.
    """
    if not os.getenv("RAPIDAPI_KEY"):
        return "RapidAPI key is missing. Please add it to the .env file."

    try:
        conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
        }
        endpoint = f"/football-get-match-detail?eventid={event_id}"
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()

        response = data.decode("utf-8")
        return f"Match event details:\n{response}"
    except Exception as e:
        return f"Error fetching match event details: {str(e)}"


@tool
def general_search(query: str) -> str:
    """
    Perform a general web search using the free DuckDuckGo Instant Answer API.

    Args:
        query: The search query.
    """
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
    }

    try:
        response = requests.get(DUCKDUCKGO_URL, params=params)
        response.raise_for_status()
        data = response.json()

        abstract = data.get("AbstractText")
        related_topics = data.get("RelatedTopics")

        if abstract:
            return abstract

        if related_topics:
            return related_topics[0].get("Text", "No detailed results found.")

        return "No relevant information found for your query."
    except requests.exceptions.RequestException as e:
        return f"Error performing the search: {str(e)}"


@tool
def get_trending_news() -> str:
    """
    Fetch trending football news.

    Returns:
        A formatted string of the top trending football news.
    """
    try:
        conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
        }
        conn.request("GET", "/football-get-trendingnews", headers=headers)
        res = conn.getresponse()
        data = res.read()
        response = json.loads(data.decode("utf-8"))

        if response.get("status") == "success":
            news = response.get("response", {}).get("news", [])
            if news:
                formatted_news = []
                for item in news[:10]:
                    title = item.get("title", "No title provided")
                    description = item.get("description", "No description available")
                    link = item.get("url", "No URL available")
                    formatted_news.append(f"Title: {title}\nDescription: {description}\nURL: {link}\n")
                return "Trending Football News:\n" + "\n".join(formatted_news)
            return "No trending news available at the moment."
        else:
            return f"Failed to fetch trending news. Reason: {response.get('message', 'Unknown error')}."
    except Exception as e:
        return f"Error fetching trending news: {str(e)}"


# Initialize the agent with tools
agent = ToolCallingAgent(
    tools=[get_weather, general_search, get_match_event, get_trending_news],
    model=model
)

# Main Function
if __name__ == "__main__":
    print("Welcome to the AI-powered assistant!")
    print("You can ask questions like 'What's the weather in Paris?' or 'Search for football players or matches.'.")
    print("Type 'exit' to quit.")

    while True:
        user_query = input("\nAsk your question: ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        # Prepend system message to user query
        user_query = f"{SYSTEM_MESSAGE}\n{user_query}"

        try:
            response = agent.run(user_query)
            print("\nResponse:")
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")



# Example queries to ask the assistant:
# who is messi
# tell me about fb barcelona
# Get match event details for event ID 4621624.
# What are the latest trending football news?
# What's the weather in Berlin?

