# **README: WanderVoice Proof of Concept (POC)**

## **Overview**
This Proof of Concept (POC) demonstrates the functionality of "WanderVoice," an AI-powered voice assistant designed to handle user queries related to:
- Real-time weather information
- Football match events
- Trending news in football
- General web search functionality

The system uses OpenAI's GPT-4 for natural language understanding, WeatherAPI for weather information, and RapidAPI for football-related data. The project serves as a foundation for expanding AI-driven voice assistant capabilities.

---

## **How It Works**
The system is built using Python and integrates the following components:
1. **FastAPI** - For handling HTTP requests and WebSocket connections.
2. **Twilio Media Streams** - For voice input during calls.
3. **OpenAI's GPT-4** - For understanding user input and generating responses.
4. **WeatherAPI** - For fetching weather updates.
5. **RapidAPI** - For football-related queries (match details, trending news).
6. **SmolAgents** - A lightweight framework for tool-based AI interactions.

### **Key Features**
- **Weather Information**: Fetches and displays real-time weather data for any location using WeatherAPI.
- **Football Match Events**: Retrieves match details (based on event IDs) using RapidAPI.
- **Trending Football News**: Lists top football news with titles, descriptions, and links via RapidAPI.
- **General Search**: Uses DuckDuckGo's free API for lightweight web search.

---

## **Setup Instructions**

### **Requirements**
Ensure the following tools and dependencies are installed:
- Python 3.9 or higher
- Virtual Environment (`venv` or similar)
- Required libraries specified in `requirements.txt`

### **Installation Steps**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/wandervoice.git
   cd wandervoice

2. Create and activate a virtual environment:
    python -m venv poc
    source poc/bin/activate  # For Linux/Mac
    poc\Scripts\activate     # For Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Add API keys to the .env file:
    OPENAI_API_KEY= key
    GPT_MODEL=gpt-4
    RAPIDAPI_KEY=3d63f108b5mshe5bba312e58b1eep124b88jsn5471d3de9c2c # https://rapidapi.com/Creativesdev/api/free-api-live-football-data/
    FREE_WEATHER_API=8a1c2fd0e1824f4bae2230449250701     # https://www.weatherapi.com/

5. Run the main application:
    python main.py

### **Sample Commands**
Here are some sample prompts you can use with the assistant:

Weather Query:
"What's the weather in Paris?"
Football Match Details:
"Get match event details for event ID 4621624."
Trending News:
"What are the latest trending football news?"
General Search:
"Who is Lionel Messi?"



### **Why Some Prompts Work and Others Don't**
API Limitations
RapidAPI:
Only specific endpoints are used for match details and news.
Prompts requiring unsupported queries might fail.
DuckDuckGo API:
Provides limited information due to its lightweight design.
WeatherAPI:
Fetches real-time data, but requires valid location input.
Solution
Use specific prompts that align with the available API endpoints, as shown in the sample commands.

### **Future Improvements**
Dynamic Prompting:
Improve handling of unsupported queries with fallback mechanisms.
Expanded API Coverage:
Add support for more endpoints or APIs to handle diverse queries.
Error Handling:
Improve error responses for unsupported or malformed prompts.



### **Files and Structure**
Key Files
app.py: Contains the AI tools and the ToolCallingAgent logic.
.env: Stores API keys and configuration variables.
requirements.txt: List of required dependencies.